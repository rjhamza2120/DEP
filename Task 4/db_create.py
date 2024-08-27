import sqlite3

conn = sqlite3.connect('patients_data.sqlite')

cursor = conn.cursor()

sql_query = """ Create Table PatientsData (
    id integer PRIMARY KEY,
    name text NOT NULL,
    disease text NOT NULL
)"""

table = """CREATE TABLE  Admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)"""

cursor.execute(sql_query)
cursor.execute(table)
