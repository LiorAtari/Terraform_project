from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import Error
import os

app = Flask(__name__)

# Database connection details
DB_HOST = '10.0.1.4'  # Replace with your actual host
DB_PORT = '5432'  # Replace with your actual port
DB_NAME = 'flask_db'  # Replace with your actual database name
DB_USER = 'postgres'  # Replace with your actual username
DB_PASSWORD = 'password'

@app.route('/', methods=['GET'])
def index():
    return render_template('flaskApp.html')

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def disconnect_from_database(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.close()

@app.route('/data', methods=['POST'])
def process_data():
    try:
        data = request.json

        name = data.get('name')
        age_value = data.get('age_value')
        time = data.get('time')

        conn = connect_to_database()
        if not conn:
            response = {
                'status': 'error',
                'message': 'Database connection error'
            }
            return jsonify(response), 500

        cur = conn.cursor()

        # Execute the INSERT statement with ON CONFLICT DO NOTHING
        insert_query = "INSERT INTO table_gifts_yovel (name, age_value, time) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
        cur.execute(insert_query, (name, age_value, time))

        # Commit the changes
        conn.commit()

        response = {
            'status': 'success',
            'name': name,
            'age_value': age_value,
            'time': time,
            'database_status': 'Data inserted successfully'
        }

        disconnect_from_database(conn, cur)
        return jsonify(response)

    except psycopg2.Error as e:
        response = {
            'status': 'error',
            'message': 'Database error',
            'error_details': str(e)
        }

        disconnect_from_database(conn, cur)
        return jsonify(response), 500

@app.route('/data/<name>', methods=['GET'])
def retrieve_data(name):
    try:
        conn = connect_to_database()
        if not conn:
            response = {
                'status': 'error',
                'message': 'Database connection error'
            }
            return jsonify(response), 500

        cur = conn.cursor()

        # Execute the SELECT statement to retrieve data based on name
        select_query = "SELECT * FROM table_gifts_yovel WHERE name = %s"
        cur.execute(select_query, (name,))
        result = cur.fetchone()

        if result:
            # Retrieve the relevant information from the database
            name = result[0]
            age_value = result[1]
            time = result[2]

            response = {
                'status': 'success',
                'name': name,
                'age_value': age_value,
                'time': time
            }
        else:
            response = {
                'status': 'error',
                'message': 'Data not found for the provided name'
            }

        disconnect_from_database(conn, cur)
        return jsonify(response)

    except psycopg2.Error as e:
        response = {
            'status': 'error',
            'message': 'Database error',
            'error_details': str(e)
        }
        disconnect_from_database(conn, cur)
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8080")
