from http.server import BaseHTTPRequestHandler
import json
import mysql.connector
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            payload = json.loads(self.rfile.read(content_length).decode('utf-8'))

            user_id = payload.get('user_id')
            new_passcode = payload.get('new_passcode')

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=int(os.environ.get("DB_PORT", 15463))
            )
            cursor = connection.cursor()

            cursor.execute("UPDATE Users SET Passcode = %s WHERE UserID = %s", (new_passcode, user_id))
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

        except Exception as e:
            if 'connection' in locals() and connection.is_connected():
                connection.rollback()
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()