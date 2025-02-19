from flask import Flask, request, jsonify, send_from_directory
import pymysql
import os
import logging

app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Config
DB_HOST = os.getenv('DB_HOST', 'obviendb-prod-db.cxy22w68otmj.us-east-2.rds.amazonaws.com')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', '12345678')
DB_NAME = os.getenv('DB_NAME', 'obviendb')

def get_db_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        logger.error(f"Database Connection Error: {e}")
        return None

@app.route("/")
def index():
    return send_from_directory('.', 'employee_search.html')

@app.route("/script.js")
def serve_js():
    return send_from_directory('.', 'script.js')

@app.route("/styles.css")
def serve_css():
    return send_from_directory('.', 'styles.css')

@app.route("/search")
def search():
    first_name = request.args.get("first_name", "").strip().lower()
    last_name = request.args.get("last_name", "").strip().lower()
    title = request.args.get("title", "").strip().lower()
    company = request.args.get("company", "").strip().lower()

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()

    sql_query = """
        SELECT `Unique Contact ID` AS id, 
               `Contact First Name` AS first_name, 
               `Primary Last Name` AS last_name, 
               `Company Name` AS company, 
               `position`
        FROM `employee_details_db`
        WHERE (%s = '' OR LOWER(`Contact First Name`) LIKE %s)
          AND (%s = '' OR LOWER(`Primary Last Name`) LIKE %s)
          AND (%s = '' OR LOWER(`position`) LIKE %s)
          AND (%s = '' OR LOWER(`Company Name`) LIKE %s)
    """
    params = [first_name, f'%{first_name}%',
              last_name, f'%{last_name}%',
              title, f'%{title}%',
              company, f'%{company}%']

    cursor.execute(sql_query, params)
    results = [{'id': row['id'],
                'name': f"{row['first_name']} {row['last_name']}",
                'company': row['company'],
                'title': row['position']} for row in cursor.fetchall()]
    connection.close()

    return jsonify(results if results else {'message': 'No results found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
