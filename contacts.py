import pandas as pd
import sqlite3

# Read the Excel file
excel_file = 'Gen1_Contact_Name_Db.xlsx'
df = pd.read_excel(excel_file)

# Create a SQLite database and connect to it
conn = sqlite3.connect('contacts.db')

# Write the data to a SQLite table
df.to_sql('contacts', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print("Data successfully loaded into SQLite database.")