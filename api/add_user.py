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
            user_id = payload.get('user_id') # If None, we create a new user

            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=os.environ.get("DB_PORT", 25060)
            )
            cursor = connection.cursor()

            if user_id:
                # Update existing user
                query = """
                    UPDATE Users 
                    SET Age = %s, WeightKG = %s, HeightCM = %s, Gender = %s, 
                        FitnessGoal = %s, CalculatedBMR = %s, TargetCalories = %s, Username = %s
                    WHERE UserID = %s
                """
                values = (
                    int(payload['age']),
                    float(payload['weight']),
                    float(payload['height']),
                    payload['gender'],
                    payload['goal'],
                    int(payload['bmr']),
                    int(payload['target_calories']),
                    payload.get('username', 'User'),
                    user_id
                )
            else:
                # Create new user
                query = """
                    INSERT INTO Users (Username, Age, WeightKG, HeightCM, Gender, FitnessGoal, CalculatedBMR, TargetCalories)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    payload.get('username', 'New User'),
                    int(payload['age']),
                    float(payload['weight']),
                    float(payload['height']),
                    payload['gender'],
                    payload['goal'],
                    int(payload['bmr']),
                    int(payload['target_calories'])
                )
            
            cursor.execute(query, values)
            connection.commit()

            msg = "Profile updated!" if user_id else "New profile created!"
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": msg}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
