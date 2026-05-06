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
            
            cursor.execute("SELECT RecipeID, RecipeName, Calories, ProteinGrams, CarbsGrams, FatsGrams FROM Recipes WHERE UserID = %s", (user_id,))
            recipes = cursor.fetchall()
            self.send_json_response(200, {"status": "success", "data": recipes})

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

            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO Recipes (UserID, RecipeName, Calories, ProteinGrams, CarbsGrams, FatsGrams) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (user_id, payload['recipe_name'], int(payload['calories']), int(payload.get('protein', 0)), int(payload.get('carbs', 0)), int(payload.get('fats', 0))))
            connection.commit()

            self.send_json_response(200, {"status": "success", "message": "Recipe added!"})

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
