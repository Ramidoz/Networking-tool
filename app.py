from flask import Flask, request, jsonify, send_from_directory
import pymysql
import pandas as pd
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variables for sensitive data
DB_HOST = os.getenv('DB_HOST', 'obviendb-prod-db.cxy22w68otmj.us-east-2.rds.amazonaws.com')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASS = os.getenv('DB_PASS', '12345678')
DB_NAME = os.getenv('DB_NAME', 'obviendb')

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db_connection():
    """Establish a connection to the RDS MySQL database."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"Error connecting to database: {e}")
        return None


@app.route('/')
def index():
    return send_from_directory('.', 'employee_search.html')


@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')


@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')


@app.route('/loader.html')
def loader():
    return send_from_directory('.', 'loader.html')


@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    logger.info(f"Searching for query: {query}")

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()
    cursor.execute("""
        SELECT `Unique Contact ID`, `Contact First Name`, `Primary Last Name`, `Company Name`, position
        FROM employee_details_db
        WHERE LOWER(`Contact First Name`) LIKE %s OR LOWER(`Primary Last Name`) LIKE %s
    """, (f'%{query}%', f'%{query}%'))

    results = [{'id': row['Unique Contact ID'],
                'name': f"{row['Contact First Name']} {row['Primary Last Name']}",
                'company': row['Company Name'],
                'title': row['position']} for row in cursor.fetchall()]
    connection.close()

    if results:
        return jsonify(results)
    else:
        return jsonify({'message': 'No results found'})


@app.route('/employee/<int:id>')
def employee(id):
    logger.info(f"Fetching employee with ID: {id}")

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM employee_details_db WHERE `Unique Contact ID` = %s", (id,))
        employee = cursor.fetchone()

        if employee:
            return jsonify({
                'id': employee['Unique Contact ID'],
                'name': f"{employee['Contact First Name']} {employee['Primary Last Name']}",
                'company': employee['Company Name'],
                'title': employee['position']
            })
        else:
            return jsonify({'error': 'Employee not found'}), 404
    except Exception as e:
        logger.error(f"Error fetching employee: {e}")
        return jsonify({'error': f'Error fetching employee details: {e}'}), 500
    finally:
        connection.close()


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)
        connection = get_db_connection()
        cursor = connection.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO employee_details_db (Contact_First_Name, Primary_Last_Name, Company_Name, Position) 
                VALUES (%s, %s, %s, %s)
            """, (row['Contact First Name'], row['Primary Last Name'], row['Company Name'], row['Position']))

        connection.commit()
        connection.close()
        return jsonify({'message': 'File uploaded and processed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal Server Error: {error}")
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f"404 Error: {error}")
    return jsonify({"error": "Resource not found."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
