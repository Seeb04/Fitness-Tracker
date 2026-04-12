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
            passcode = payload.get('passcode')

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=int(os.environ.get("DB_PORT", 15463))
            )
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT UserID, Username FROM Users WHERE UserID = %s AND Passcode = %s", (user_id, passcode))
            user = cursor.fetchone()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if user:
                self.wfile.write(json.dumps({"status": "success", "message": "Login successful", "data": user}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"status": "error", "message": "Incorrect passcode"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()