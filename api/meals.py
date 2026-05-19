from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from ._db import get_db_connection

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            user_id = query_params.get('user_id', ['1'])[0]

            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Fetch all meals for this user. Frontend filters by date if needed.
            cursor.execute("SELECT MealID, UserID, DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, FoodItem, Calories, ProteinGrams, CarbsGrams, FatsGrams FROM Meals WHERE UserID = %s ORDER BY LogDate DESC", (user_id,))
            meals = cursor.fetchall()
            
            self.send_json_response(200, {"status": "success", "data": meals})

        except Exception as e:
            self.send_json_response(500, {"status": "error", "message": str(e)})
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
            user_id = payload.get('user_id', 1)

            # Edge casing: Prevent negative values
            if int(payload.get('calories', 0)) < 0 or int(payload.get('protein', 0)) < 0 or int(payload.get('carbs', 0)) < 0 or int(payload.get('fats', 0)) < 0:
                return self.send_json_response(400, {"status": "error", "message": "Nutritional values cannot be negative"})

            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO Meals (UserID, LogDate, FoodItem, Calories, ProteinGrams, CarbsGrams, FatsGrams) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                user_id, 
                payload['date'], 
                payload['food'], 
                int(payload['calories']),
                int(payload.get('protein', 0)), 
                int(payload.get('carbs', 0)), 
                int(payload.get('fats', 0))
            )
            cursor.execute(insert_query, values)
            connection.commit()

            self.send_json_response(200, {"status": "success", "message": "Meal inserted!"})

        except Exception as e:
            self.send_json_response(500, {"status": "error", "message": str(e)})
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def send_json_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
