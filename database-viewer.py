import sqlite3
# This is just a test file to see if the data is saved correctly!
conn = sqlite3.connect('results-database/students.sqlite3')
cursor = conn.cursor()
cursor.execute('SELECT * FROM students_data')
rows = cursor.fetchall()

print("Data in students_data table:")
for row in rows[:10]:
    i , j ,k = row
    print(f"Roll Number: {i}, Category of Admission Test: {j}, Marks Obtained: {k}")

conn.close()