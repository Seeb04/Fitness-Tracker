from http.server import BaseHTTPRequestHandler
import json
from ._db import get_db_connection

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            
            user_id = payload.get('user_id')
            entry_id = payload.get('entry_id')
            entry_type = payload.get('type')
            
            if not user_id or not entry_id or not entry_type:
                raise ValueError("Missing required fields")

            connection = get_db_connection()
            cursor = connection.cursor()

            if entry_type == 'meal':
                query = "DELETE FROM Meals WHERE MealID = %s AND UserID = %s"
            elif entry_type == 'workout':
                query = "DELETE FROM Workouts WHERE WorkoutID = %s AND UserID = %s"
            else:
                raise ValueError("Invalid entry type")

            cursor.execute(query, (entry_id, user_id))
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Entry deleted successfully"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
