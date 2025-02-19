from flask import Flask, request, jsonify, send_from_directory
import pymysql
import pandas as pd
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

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

@app.route("/loader.html")
def serve_loader():
    return send_from_directory('.', 'loader.html')

@app.route("/health")
def health_check():
    return "OK", 200  # Health check route

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads and inserts data into MySQL RDS."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)  # Save the file temporarily

    try:
        # Read Excel file using pandas
        df = pd.read_excel(filepath)

        # Validate required columns (must match database)
        required_columns = {'Contact First Name', 'Primary Last Name', 'Company Name', 'Position'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': 'Invalid file format. Missing required columns.'}), 400

        connection = get_db_connection()
        if connection is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor()

        # Insert data into MySQL RDS
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO employee_details_db (Contact_First_Name, Primary_Last_Name, Company_Name, Position) 
                VALUES (%s, %s, %s, %s)
            """, (row['Contact First Name'], row['Primary Last Name'], row['Company Name'], row['Position']))

        connection.commit()
        connection.close()

        # Optional: Delete the file after processing
        os.remove(filepath)

        return jsonify({'message': 'File uploaded and processed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
