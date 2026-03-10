from flask import Flask, jsonify
import pyodbc
import os

app = Flask(__name__)

# Database configuration (use environment variables in production)
DB_SERVER = "mysqlserverhehehehe.database.windows.net"
DB_NAME = "mysqldatabase"
DB_USER = "4dm1n157r470r"
DB_PASSWORD = "4-v3ry-53cr37-p455w0rd"

# ODBC connection string for Azure SQL
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
)

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn


@app.route("/")
def home():
    return "Hello from Flask on Azure App Service!"


@app.route("/health")
def health():
    return {"status": "running"}


@app.route("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT GETDATE();")
        row = cursor.fetchone()

        conn.close()

        return jsonify({
            "database_status": "connected",
            "server_time": str(row[0])
        })

    except Exception as e:
        return jsonify({
            "database_status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
