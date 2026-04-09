from http.server import BaseHTTPRequestHandler
import json
import mysql.connector
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Read the data sent from the website
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))

            # 2. Connect to the Aiven MySQL Database
            # We use os.environ so your password isn't visible in the code!
            connection = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                port=os.environ.get("DB_PORT", 3306)
            )
            
            cursor = connection.cursor()

            # 3. Write and execute the SQL query
            # We use %s to safely insert data and prevent SQL injection hackers
            insert_query = """
                INSERT INTO Meals (LogDate, FoodItem, CaloriesIn) 
                VALUES (%s, %s, %s)
            """
            
            # The values come directly from the website's payload
            values = (payload['date'], payload['food'], int(payload['calories']))
            cursor.execute(insert_query, values)
            connection.commit() # Save the changes!

            # 4. Tell the website it worked
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "Meal inserted!"}).encode('utf-8'))

        except Exception as e:
            # If something breaks, tell the website what went wrong
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()