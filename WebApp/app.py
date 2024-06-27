from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def calculate_percentile(marks, category):
    conn = sqlite3.connect('students.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f"SELECT marks_obtained FROM students_data WHERE category_of_admission_test = '{category}'")
    all_marks = [row[0] for row in cursor.fetchall()]
    total_students = len(all_marks)
    students_below = len([m for m in all_marks if m < marks])
    percentile = (students_below / total_students) * 100
    conn.close()
    return round(percentile, 2)

def calculate_merit_position(marks, category):
    conn = sqlite3.connect('students.sqlite3')
    cursor = conn.cursor()
    print(category)
    cursor.execute(f"SELECT marks_obtained FROM students_data WHERE category_of_admission_test = '{category}' ORDER BY marks_obtained DESC")
    all_marks = [row[0] for row in cursor.fetchall()]
    merit_position = all_marks.index(marks) + 1
    conn.close()
    return merit_position, len(all_marks)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    roll_number = request.form['roll_number']
    
    conn = sqlite3.connect('students.sqlite3')
    cursor = conn.cursor()
    print(roll_number)
    cursor.execute('SELECT marks_obtained,category_of_admission_test FROM students_data WHERE roll_number = ? ', (roll_number,))
    result = cursor.fetchone()
    print(result)
    
    if result:
        marks_obtained = result[0]
        print(result)
        category = result[1]
        percentile = calculate_percentile(marks_obtained, category)
        merit_position, total_students = calculate_merit_position(marks_obtained, category)
        
        return render_template('result.html', roll_number=roll_number, category=category, marks_obtained=marks_obtained, percentile=percentile, merit_position=merit_position, total_students=total_students)
    else:
        return "No data found for the given roll number and category.", 404

if __name__ == '__main__':
    app.run(debug=True)
