import sqlite3
import pandas as pd
def read_database():
    conn = sqlite3.connect('results-database/students.sqlite3')
    df = pd.read_sql('SELECT * FROM students_data', con=conn)
    print(df)
    return df

def find_merit_position(df, roll):
    df_sorted = df.sort_values(by='Marks Obtained', ascending=False).reset_index(drop=True)
    meritPosition = df_sorted[df_sorted['Roll Number'] == int(roll)].index[0] + 1
    print(f"Your merit position is: {meritPosition}")
    percentile = 100 - (meritPosition / len(df)) * 100
    print(f"Your percentile is: {round(percentile,2)}%")
    return meritPosition, percentile