import sqlite3

connection = sqlite3.connect('employees.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    job_title TEXT
)
''')

sample_data = [
    ('Aromal Aravind', 'aromal@example.com', '1234567890', 'Software Engineer'),
    ('John Doe', 'john.doe@example.com', '0987654321', 'Project Manager'),
    ('Jane Smith', 'jane.smith@example.com', '1122334455', 'Designer')
]

cursor.executemany('INSERT INTO employees (name, email, phone, job_title) VALUES (?, ?, ?, ?)', sample_data)

connection.commit()
connection.close()