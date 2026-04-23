from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from ._db import get_db_connection

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            action = query_params.get('action', [None])[0]
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            if action == 'exercises':
                # get_exercises.py
                cursor.execute("SELECT ExerciseID, Name, MuscleGroup FROM Exercises ORDER BY Name")
                data = cursor.fetchall()
            else:
                # get_workouts.py
                user_id = query_params.get('user_id', ['1'])[0]
                days = query_params.get('days', [None])[0]
                if days:
                    query = "SELECT WorkoutID, DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, WorkoutCategory, DurationMinutes, CaloriesBurned FROM Workouts WHERE UserID = %s AND LogDate >= DATE_SUB(CURDATE(), INTERVAL %s DAY) ORDER BY LogDate DESC, WorkoutID DESC"
                    cursor.execute(query, (user_id, int(days)))
                else:
                    query = "SELECT WorkoutID, DATE_FORMAT(LogDate, '%Y-%m-%d') as LogDate, WorkoutCategory, DurationMinutes, CaloriesBurned FROM Workouts WHERE UserID = %s ORDER BY LogDate DESC, WorkoutID DESC LIMIT 10"
                    cursor.execute(query, (user_id,))
                data = cursor.fetchall()

            self.send_json_response(200, {"status": "success", "data": data})

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

            insert_query = "INSERT INTO Workouts (UserID, LogDate, WorkoutCategory, DurationMinutes, CaloriesBurned) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (user_id, payload['date'], payload['category'], int(payload['duration']), int(payload['calories'])))
            connection.commit()

            self.send_json_response(200, {"status": "success", "message": "Workout inserted!"})

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
