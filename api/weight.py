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
            
            cursor.execute("SELECT DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, WeightKG FROM WeightLogs WHERE UserID = %s ORDER BY LogDate DESC LIMIT 30", (user_id,))
            weights = cursor.fetchall()
            for w in weights: w['WeightKG'] = float(w['WeightKG'])
            
            self.send_json_response(200, {"status": "success", "data": weights})

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

            # Check if a weight entry already exists for this user and date
            cursor.execute("SELECT 1 FROM WeightLogs WHERE UserID = %s AND LogDate = %s", (user_id, payload['date']))
            if cursor.fetchone():
                # Update existing record
                cursor.execute("UPDATE WeightLogs SET WeightKG = %s WHERE UserID = %s AND LogDate = %s", (payload['weight'], user_id, payload['date']))
            else:
                # Insert new record
                cursor.execute("INSERT INTO WeightLogs (UserID, LogDate, WeightKG) VALUES (%s, %s, %s)", (user_id, payload['date'], payload['weight']))

            # Sync the new weight to the main Users table
            cursor.execute("UPDATE Users SET WeightKG = %s WHERE UserID = %s", (payload['weight'], user_id))
            
            connection.commit()
            self.send_json_response(200, {"status": "success", "message": "Weight logged!"})

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
