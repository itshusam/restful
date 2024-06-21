from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="fitness"
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

def close_connection(conn):
    if conn:
        conn.close()

conn = connect_to_database()

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    query = "INSERT INTO Members (name) VALUES (%s)"
    values = (name,)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Member added successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    query = "SELECT * FROM Members WHERE id = %s"
    values = (id,)

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, values)
        member = cursor.fetchone()

        if not member:
            return jsonify({'message': 'Member not found'}), 400

        return jsonify(member), 400
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    query = "UPDATE Members SET name = %s WHERE id = %s"
    values = (name, id)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Member not found'}), 404

        return jsonify({'message': 'Member updated successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    query = "DELETE FROM Members WHERE id = %s"
    values = (id,)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Member not found'}), 400

        return jsonify({'message': 'Member deleted successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()


@app.route('/workout_sessions', methods=['POST'])
def schedule_workout_session():
    data = request.get_json()
    date = data.get('date')
    member_id = data.get('member_id')

    if not date or not member_id:
        return jsonify({'error': 'Date and member_id are required'}), 400

    query = "INSERT INTO WorkoutSessions (date, member_id) VALUES (%s, %s)"
    values = (date, member_id)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Workout session scheduled successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/workout_sessions/<int:member_id>', methods=['GET'])
def get_workout_sessions(member_id):
    query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
    values = (member_id,)

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, values)
        sessions = cursor.fetchall()

        if not sessions:
            return jsonify({'message': 'No workout sessions found for this member'}), 400

        return jsonify(sessions), 400
    except Error as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    data = request.get_json()
    date = data.get('date')

    if not date:
        return jsonify({'error': 'Date is required'}), 400

    query = "UPDATE WorkoutSessions SET date = %s WHERE id = %s"
    values = (date, id)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Workout session not found'}), 400

        return jsonify({'message': 'Workout session updated successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()

@app.route('/workout_sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    query = "DELETE FROM WorkoutSessions WHERE id = %s"
    values = (id,)

    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Workout session not found'}), 400

        return jsonify({'message': 'Workout session deleted successfully'}), 400
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()



if __name__ == '__main__':
    app.run(debug=True)