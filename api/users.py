from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from ._db import get_db_connection

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            user_id = query_params.get('user_id', [None])[0]
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            if user_id:
                # get_user.py
                query = "SELECT UserID, Username, Age, WeightKG, HeightCM, Gender, FitnessGoal, CalculatedBMR, TargetCalories FROM Users WHERE UserID = %s"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()
                if user:
                    if user.get('WeightKG') is not None: user['WeightKG'] = float(user['WeightKG'])
                    if user.get('HeightCM') is not None: user['HeightCM'] = float(user['HeightCM'])
                    self.send_json_response(200, {"status": "success", "data": user})
                else:
                    self.send_json_response(404, {"status": "error", "message": "User not found"})
            else:
                # get_users.py
                cursor.execute("SELECT UserID, Username FROM Users ORDER BY Username")
                users = cursor.fetchall()
                self.send_json_response(200, {"status": "success", "data": users})

        except Exception as e:
            self.send_json_response(500, {"status": "error", "message": str(e)})
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def do_POST(self):
        try:
            query_params = parse_qs(urlparse(self.path).query)
            action = query_params.get('action', [None])[0]
            
            content_length = int(self.headers['Content-Length'])
            payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            if action == 'login':
                # login.py
                user_id = payload.get('user_id')
                passcode = payload.get('passcode')
                cursor.execute("SELECT UserID, Username FROM Users WHERE UserID = %s AND Passcode = %s", (user_id, passcode))
                user = cursor.fetchone()
                if user:
                    self.send_json_response(200, {"status": "success", "message": "Login successful", "data": user})
                else:
                    self.send_json_response(200, {"status": "error", "message": "Incorrect passcode"})
            
            elif action == 'update_passcode':
                # update_passcode.py
                user_id = payload.get('user_id')
                new_passcode = payload.get('new_passcode')
                cursor.execute("UPDATE Users SET Passcode = %s WHERE UserID = %s", (new_passcode, user_id))
                connection.commit()
                self.send_json_response(200, {"status": "success"})
            
            else:
                # add_user.py
                user_id = payload.get('user_id')
                if user_id:
                    # Update
                    query = "UPDATE Users SET Age = %s, WeightKG = %s, HeightCM = %s, Gender = %s, FitnessGoal = %s, CalculatedBMR = %s, TargetCalories = %s, Username = %s WHERE UserID = %s"
                    values = (int(payload['age']), float(payload['weight']), float(payload['height']), payload['gender'], payload['goal'], int(payload['bmr']), int(payload['target_calories']), payload.get('username', 'User'), user_id)
                    msg = "Profile updated!"
                else:
                    # Create
                    query = "INSERT INTO Users (Username, Age, WeightKG, HeightCM, Gender, FitnessGoal, CalculatedBMR, TargetCalories, Passcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (payload.get('username', 'New User'), int(payload['age']), float(payload['weight']), float(payload['height']), payload['gender'], payload['goal'], int(payload['bmr']), int(payload['target_calories']), '0000')
                    msg = "New profile created!"
                
                cursor.execute(query, values)
                connection.commit()
                self.send_json_response(200, {"status": "success", "message": msg})

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
