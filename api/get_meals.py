from http.server import BaseHTTPRequestHandler
import json
import mysql.connector
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=os.environ.get("DB_PORT", 25060)
            )
            # dictionary=True makes the results format as JSON objects instead of raw arrays
            cursor = connection.cursor(dictionary=True)
            
            # We use DATE_FORMAT so Python doesn't crash trying to serialize a raw Date object
            query = """
                SELECT DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, 
                    FoodItem, Calories, ProteinGrams, CarbsGrams, FatsGrams 
                FROM Meals WHERE UserID = 1 ORDER BY MealID DESC LIMIT 10
            """
            cursor.execute(query)
            meals = cursor.fetchall()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": meals}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()