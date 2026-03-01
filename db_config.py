import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abi@naya@030610",  # Replace this
            database="ai_study_companion"
        )
        return connection
    except Error as e:
        print("Database Error:", e)
        return None
