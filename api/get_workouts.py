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
            days = query_params.get('days', [None])[0]

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=os.environ.get("DB_PORT", 15463)
            )
            cursor = connection.cursor(dictionary=True)
            
            if days:
                query = """
                    SELECT WorkoutID, DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, 
                        WorkoutCategory, DurationMinutes, CaloriesBurned 
                    FROM Workouts WHERE UserID = %s AND LogDate >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
                    ORDER BY LogDate DESC, WorkoutID DESC
                """
                cursor.execute(query, (user_id, int(days)))
            else:
                query = """
                    SELECT WorkoutID, DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, 
                        WorkoutCategory, DurationMinutes, CaloriesBurned 
                    FROM Workouts WHERE UserID = %s ORDER BY LogDate DESC, WorkoutID DESC LIMIT 10
                """
                cursor.execute(query, (user_id,))
                
            workouts = cursor.fetchall()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": workouts}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
