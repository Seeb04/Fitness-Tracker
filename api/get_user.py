from http.server import BaseHTTPRequestHandler
import json
import mysql.connector
import os
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            user_id = query_params.get('user_id', ['1'])[0]

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=int(os.environ.get("DB_PORT", 15463))
            )
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT UserID, Username, Age, WeightKG, HeightCM, Gender, FitnessGoal, CalculatedBMR, TargetCalories FROM Users WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                if user.get('WeightKG') is not None:
                    user['WeightKG'] = float(user['WeightKG'])
                if user.get('HeightCM') is not None:
                    user['HeightCM'] = float(user['HeightCM'])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "data": user}).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "User not found"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
