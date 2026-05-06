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
            
            cursor.execute("SELECT RoutineID, RoutineName FROM Routines WHERE UserID = %s AND IsActive = TRUE LIMIT 1", (user_id,))
            routine = cursor.fetchone()

            if not routine:
                return self.send_json_response(200, {"status": "success", "data": None})

            cursor.execute("SELECT DayID, DayName, DayOrder FROM RoutineDays WHERE RoutineID = %s ORDER BY DayOrder", (routine['RoutineID'],))
            days = cursor.fetchall()

            for day in days:
                query = """
                    SELECT re.TargetSets, re.TargetReps, e.Name as ExerciseName, e.MuscleGroup 
                    FROM RoutineExercises re
                    JOIN Exercises e ON re.ExerciseID = e.ExerciseID
                    WHERE re.DayID = %s
                """
                cursor.execute(query, (day['DayID'],))
                day['exercises'] = cursor.fetchall()

            routine['days'] = days
            self.send_json_response(200, {"status": "success", "data": routine})

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
            user_id = payload.get('user_id')
            routine_name = payload.get('routine_name')
            days = payload.get('days', [])

            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("UPDATE Routines SET IsActive = FALSE WHERE UserID = %s", (user_id,))
            cursor.execute("INSERT INTO Routines (UserID, RoutineName, IsActive) VALUES (%s, %s, TRUE)", (user_id, routine_name))
            routine_id = cursor.lastrowid

            for day_index, day in enumerate(days):
                cursor.execute("INSERT INTO RoutineDays (RoutineID, DayName, DayOrder) VALUES (%s, %s, %s)", (routine_id, day['day_name'], day_index + 1))
                day_id = cursor.lastrowid
                for ex in day.get('exercises', []):
                    cursor.execute("INSERT INTO RoutineExercises (DayID, ExerciseID, TargetSets, TargetReps) VALUES (%s, %s, %s, %s)", (day_id, ex['exercise_id'], ex['sets'], ex['reps']))

            connection.commit()
            self.send_json_response(200, {"status": "success", "message": "Routine built and activated!"})

        except Exception as e:
            if 'connection' in locals() and connection.is_connected(): connection.rollback()
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
