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

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=os.environ.get("DB_PORT", 15463)
            )
            
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO Workouts (UserID, LogDate, WorkoutCategory, DurationMinutes, CaloriesBurned) 
                VALUES (1, %s, %s, %s, %s)
            """
            
            values = (
                payload['date'], 
                payload['category'], 
                int(payload['duration']),
                int(payload['calories'])
            )
            cursor.execute(insert_query, values)
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Workout inserted!"}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
