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
                port=int(os.environ.get("DB_PORT", 15463)) # Still using the int() fix!
            )
            cursor = connection.cursor(dictionary=True)
            
            # 1. Get the Active Routine
            cursor.execute("SELECT RoutineID, RoutineName FROM Routines WHERE UserID = %s AND IsActive = TRUE LIMIT 1", (user_id,))
            routine = cursor.fetchone()

            if not routine:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "data": None}).encode('utf-8'))
                return

            # 2. Get the Days
            cursor.execute("SELECT DayID, DayName, DayOrder FROM RoutineDays WHERE RoutineID = %s ORDER BY DayOrder", (routine['RoutineID'],))
            days = cursor.fetchall()

            # 3. Get the Exercises for each day
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

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "data": routine}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()