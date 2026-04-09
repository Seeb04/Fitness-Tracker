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
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT Age, WeightKG, HeightCM, Gender, FitnessGoal, CalculatedBMR, TargetCalories FROM Users WHERE UserID = 1"
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "data": user}).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "User not found"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
