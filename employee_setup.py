import sqlite3

# Drop existing table
connection = sqlite3.connect('employees.db')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS employees')
connection.commit()
connection.close()

# Create new table
connection = sqlite3.connect('employees.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    contact_first_name TEXT,
    middle_name_initial TEXT,
    primary_last_name TEXT,
    secondary_last_name TEXT,
    other_name TEXT,
    unique_contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_names_order TEXT,
    address_1 TEXT,
    address_2 TEXT,
    address_3 TEXT,
    city TEXT,
    region_name TEXT,
    county TEXT,
    state TEXT,
    postal_zip TEXT,
    country TEXT,
    address_type TEXT,
    original_region_id TEXT,
    current_region_id TEXT,
    entry_date TEXT,
    entry_time TEXT,
    last_modification_date TEXT,
    last_modification_time TEXT,
    source_id_contact TEXT,
    private_owner_record TEXT,
    private_owner_id TEXT,
    revision_made TEXT,
    source_license_type TEXT,
    source_license_level TEXT,
    link_to_source TEXT,
    company_name TEXT,
    company_id TEXT,
    position TEXT,
    title_id TEXT
)
''')
connection.commit()
connection.close()

# Insert sample data
connection = sqlite3.connect('employees.db')
cursor = connection.cursor()
sample_data = [
    ('Aromal', 'A.', 'Aravind', 'Nair', 'Aro', None, 'First', '123 Street', 'Suite 1', 'Building A', 'CityX', 'RegionY', 'CountyZ', 'StateA', '12345', 'CountryB', 'Home', 'Region1', 'Region2', '2024-12-01', '10:00:00', '2024-12-07', '15:00:00', 'Source1', 'Yes', 'Owner1', 'Rev1', 'LicenseType1', 'Level1', 'http://example.com', 'TechCorp', 'C001', 'Software Engineer', 'T001'),
    ('Sumit', 'B.', 'Doe', 'Poojary', 'Johnny', None, 'Last', '456 Avenue', 'Suite 2', 'Building B', 'CityY', 'RegionZ', 'CountyA', 'StateB', '67890', 'CountryC', 'Office', 'Region3', 'Region4', '2024-11-01', '11:00:00', '2024-12-06', '14:00:00', 'Source2', 'No', 'Owner2', 'Rev2', 'LicenseType2', 'Level2', 'http://example.org', 'Business Inc.', 'C002', 'Project Manager', 'T002'),
    ('Lakshmi', 'C.', 'Aromal', 'Iyer', 'Janey', None, 'Middle', '789 Boulevard', 'Suite 3', 'Building C', 'CityZ', 'RegionA', 'CountyB', 'StateC', '54321', 'CountryD', 'Other', 'Region5', 'Region6', '2024-10-01', '12:00:00', '2024-12-05', '13:00:00', 'Source3', 'Yes', 'Owner3', 'Rev3', 'LicenseType3', 'Level3', 'http://example.net', 'Design Studio', 'C003', 'Designer', 'T003')
]
cursor.executemany('''
INSERT INTO employees (
    contact_first_name, middle_name_initial, primary_last_name, secondary_last_name, other_name, unique_contact_id,
    contact_names_order, address_1, address_2, address_3, city, region_name, county, state, postal_zip, country,
    address_type, original_region_id, current_region_id, entry_date, entry_time, last_modification_date, last_modification_time,
    source_id_contact, private_owner_record, private_owner_id, revision_made, source_license_type, source_license_level,
    link_to_source, company_name, company_id, position, title_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', sample_data)
connection.commit()
connection.close()