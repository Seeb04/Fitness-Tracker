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
            routine_name = payload.get('routine_name')
            days = payload.get('days', []) # A list of days, which contain a list of exercises

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=int(os.environ.get("DB_PORT", 15463))
            )
            cursor = connection.cursor()

            # 1. Deactivate any previously active routines for this user
            cursor.execute("UPDATE Routines SET IsActive = FALSE WHERE UserID = %s", (user_id,))
            
            # 2. Insert the New Routine (and set it as the active one)
            cursor.execute("INSERT INTO Routines (UserID, RoutineName, IsActive) VALUES (%s, %s, TRUE)", (user_id, routine_name))
            routine_id = cursor.lastrowid

            # 3. Loop through the submitted Days
            for day_index, day in enumerate(days):
                cursor.execute("INSERT INTO RoutineDays (RoutineID, DayName, DayOrder) VALUES (%s, %s, %s)", 
                            (routine_id, day['day_name'], day_index + 1))
                day_id = cursor.lastrowid
                
                # 4. Loop through the Exercises for this specific Day
                for ex in day.get('exercises', []):
                    cursor.execute("INSERT INTO RoutineExercises (DayID, ExerciseID, TargetSets, TargetReps) VALUES (%s, %s, %s, %s)",
                                (day_id, ex['exercise_id'], ex['sets'], ex['reps']))

            # If all loops finish without crashing, commit the entire transaction!
            connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Routine built and activated!"}).encode('utf-8'))

        except Exception as e:
            # If ANYTHING fails, rollback all changes so we don't get half-built data
            if 'connection' in locals() and connection.is_connected():
                connection.rollback()
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()