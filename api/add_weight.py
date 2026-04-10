from http.server import BaseHTTPRequestHandler
import json
import mysql.connector
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            
            user_id = payload.get('user_id')
            weight = payload.get('weight')
            date = payload.get('date')
            
            if not user_id or weight is None or not date:
                raise ValueError("Missing required fields")

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=int(os.environ.get("DB_PORT", 15463))
            )
            cursor = connection.cursor()

            # 1. Insert into WeightLogs
            query_log = "INSERT INTO WeightLogs (UserID, LogDate, WeightKG) VALUES (%s, %s, %s)"
            cursor.execute(query_log, (user_id, date, weight))
            
            # 2. Update Users table with the latest weight
            query_update_user = "UPDATE Users SET WeightKG = %s WHERE UserID = %s"
            cursor.execute(query_update_user, (weight, user_id))
            
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Weight logged and profile updated"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
