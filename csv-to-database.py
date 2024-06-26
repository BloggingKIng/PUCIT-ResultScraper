import pandas as pd
import sqlite3

csv_file = 'results/pucit_result.csv' 
df = pd.read_csv(csv_file)
df.drop_duplicates(subset=['Roll Number'], inplace=True)

conn = sqlite3.connect('results-database/students.sqlite3') 
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS students_data (
    roll_number INTEGER PRIMARY KEY,
    category_of_admission_test TEXT NOT NULL,
    marks_obtained INTEGER NOT NULL
)
'''
cursor.execute(create_table_query)

for index, row in df.iterrows():
    cursor.execute('''
    INSERT INTO students_data (roll_number, category_of_admission_test, marks_obtained)
    VALUES (?, ?, ?)
    ''', (row['Roll Number'], row['Name of Category of Admission Test'], row['Marks Obtained']))

conn.commit()
conn.close()
