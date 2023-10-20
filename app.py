import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def getdbconnect():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "admin",
        "database": "SSIS",
    }
    return mysql.connector.connect(**db_config)


@app.route('/')
def index():
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'year_level': row[3],
                 'gender': row[4], 'coursecode': row[5]} for row in cursor.fetchall()]

    cursor.execute("SELECT coursecode, coursename FROM Courses")
    courses = dict([(row[0], row[1]) for row in cursor.fetchall()])
    conn.close()

    for student in students:
        student['coursename'] = courses.get(student['coursecode'])

    message = request.args.get('message')
    return render_template('index.html', students=students, message=message)


@app.route('/listCourses')
def listCourses():
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Courses")
    courses = [{'coursecode': row[0], 'coursename': row[1],
                'collegecode': row[2]} for row in cursor.fetchall()]

    cursor.execute("SELECT collegecode, collegename FROM Colleges")
    colleges = dict([(row[0], row[1]) for row in cursor.fetchall()])
    conn.close()
    for course in courses:
        course['collegename'] = colleges.get(course['collegecode'])

    message = request.args.get('message')
    return render_template('listCourses.html', courses=courses, message=message)


@app.route('/listColleges')
def listColleges():
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT collegecode, collegename FROM Colleges")
    colleges = [{'collegecode': row[0], 'collegename': row[1]}
                for row in cursor.fetchall()]
    conn.close()
    message = request.args.get('message')
    print (message)
    return render_template('listColleges.html', colleges=colleges, message=message)


@app.route('/addStudent', methods=['GET', 'POST'])
def addStudent():

    if request.method == 'POST':
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year_level = request.form.get('year_level')
        gender = request.form.get('gender')
        coursecode = request.form.get('coursecode')

        conn = getdbconnect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM Students WHERE id=%s", (id,))
        existing_student = cursor.fetchone()

        if existing_student:
            message = 'A student with the same ID already exists.'
            conn.close()
            return render_template('addStudent.html', message=message)

        values = (id, first_name, last_name, year_level, gender, coursecode)
        cursor.execute(
            "INSERT INTO Students (id, first_name, last_name, year_level, gender, coursecode) VALUES (%s, %s, %s, %s, %s, %s)", values)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT coursecode, coursename FROM Courses")
    courses = [{'coursecode': row[0], 'coursename': row[1]}
               for row in cursor.fetchall()]
    conn.close()
    return render_template('addStudent.html', courses=courses)


@app.route('/addCourse', methods=['GET', 'POST'])
def addCourse():
    if request.method == 'POST':
        coursecode = request.form.get('coursecode')
        coursename = request.form.get('coursename')
        collegecode = request.form.get('collegecode')
        conn = getdbconnect()
        cursor = conn.cursor()
        values = (coursecode, coursename, collegecode)
        cursor.execute(
            "INSERT INTO Courses (coursecode, coursename, collegecode) VALUES (%s, %s, %s)", values)
        conn.commit()
        conn.close()
        return redirect(url_for('listCourses'))

    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT collegecode, collegename FROM Colleges")
    colleges = [{'collegecode': row[0], 'collegename': row[1]}
                for row in cursor.fetchall()]
    conn.close()

    return render_template('addCourse.html', colleges=colleges)


@app.route('/addCollege', methods=['GET', 'POST'])
def addCollege():
    if request.method == 'POST':
        collegecode = request.form.get('collegecode')
        collegename = request.form.get('collegename')
        conn = getdbconnect()
        cursor = conn.cursor()
        values = (collegecode, collegename)
        cursor.execute(
            "INSERT INTO Colleges (collegecode, collegename) VALUES (%s, %s)", values)
        conn.commit()
        conn.close()
        return redirect(url_for('listColleges'))

    return render_template('addCollege.html')


@app.route('/updateStudent/<string:id>', methods=['GET', 'POST'])
def updateStudent(id):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE id=%s", (id,))

    row = cursor.fetchone()
    if row:
        student = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'year_level': row[3],
            'gender': row[4],
            'coursecode': row[5]
        }
    else:
        student = None

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year_level = request.form.get('year_level')
        gender = request.form.get('gender')
        coursecode = request.form.get('coursecode')

        cursor.execute("UPDATE Students SET first_name=%s, last_name=%s, year_level=%s, gender=%s, coursecode=%s WHERE id=%s",
                       (first_name, last_name, year_level, gender, coursecode, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM Courses")
    courses = [{'coursecode': row[0], 'coursename': row[1],
                'collegecode': row[2]} for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return render_template('updateStudent.html', student=student, courses=courses)


@app.route('/updateCourse/<string:coursecode>', methods=['GET', 'POST'])
def updateCourse(coursecode):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Courses WHERE coursecode=%s", (coursecode,))
    # course = cursor.fetchone()
    row = cursor.fetchone()
    if row:
        course = {
            'coursecode': row[0],
            'coursename': row[1],
            'collegecode': row[2]
        }
    else:
        course = None

    if request.method == 'POST':
        coursename = request.form.get('coursename')
        collegecode = request.form.get('collegecode')

        cursor.execute("UPDATE Courses SET coursename=%s, collegecode=%s WHERE coursecode=%s",
                       (coursename, collegecode, coursecode))
        conn.commit()
        conn.close()
        return redirect(url_for('listCourses'))

    cursor.execute("SELECT collegecode, collegename FROM Colleges")
    colleges = [{'collegecode': row[0], 'collegename': row[1]}
                for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return render_template('updateCourse.html', course=course, colleges=colleges)


@app.route('/updateCollege/<string:collegecode>', methods=['GET', 'POST'])
def updateCollege(collegecode):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Colleges WHERE collegecode=%s", (collegecode,))
    college = cursor.fetchone()

    if request.method == 'POST':
        collegename = request.form.get('collegename')

        cursor.execute("UPDATE Colleges SET collegename=%s WHERE collegecode=%s",
                       (collegename, collegecode))
        conn.commit()
        conn.close()
        return redirect(url_for('listColleges'))

    conn.commit()
    conn.close()
    return render_template('updateCollege.html', college=college)


@app.route('/deleteStudent/<string:id>')
def deleteStudent(id):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/deleteCourse/<string:coursecode>')
def deleteCourse(coursecode):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students WHERE coursecode=%s", (coursecode,))
    students = cursor.fetchall()

    if students:
        message = 'Cannot delete course with students enrolled'
        print("In delete", message)
        return redirect(url_for('listCourses', message=message))
    else:
        cursor.execute(
            "DELETE FROM Courses WHERE coursecode=%s", (coursecode,))
        conn.commit()

    conn.close()
    return redirect(url_for('listCourses'))


@app.route('/deleteCollege/<string:collegecode>')
def deleteCollege(collegecode):
    conn = getdbconnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Courses WHERE collegecode=%s", (collegecode,))
    courses = cursor.fetchall()

    if courses:
        message = 'Cannot delete College with courses attached.'
        print("In delete", message)
        return redirect(url_for('listColleges', message=message))
    else:
        cursor.execute(
            "DELETE FROM Colleges WHERE collegecode=%s", (collegecode,))
        conn.commit()

    conn.commit()
    conn.close()
    return redirect(url_for('listColleges'))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    conn = getdbconnect()
    cursor = conn.cursor()

    
    query = "%" + query.lower() + "%"
    cursor.execute("SELECT * FROM Colleges WHERE LOWER(collegecode) LIKE %s OR LOWER(collegename) LIKE %s", (query, query))
    
    search_results = [{'collegecode': row[0], 'collegename': row[1]} for row in cursor.fetchall()]

    conn.close()

    return render_template('searchCollege.html', search_results=search_results)


@app.route('/search-courses', methods=['GET'])
def search_courses():
    query = request.args.get('query')

    conn = getdbconnect()
    cursor = conn.cursor()

    query = "%" + query.lower() + "%"
    cursor.execute("SELECT * FROM Courses WHERE LOWER(coursecode) LIKE %s OR LOWER(coursename) LIKE %s OR LOWER(collegecode) LIKE %s", (query, query, query))
    
    search_results = [{'coursecode': row[0], 'coursename': row[1], 'collegecode': row[2]} for row in cursor.fetchall()]

    conn.close()

    return render_template('searchCourses.html', search_results=search_results)


@app.route('/search-students', methods=['GET'])
def search_students():
    query = request.args.get('query')

    conn = getdbconnect()
    cursor = conn.cursor()

    query = "%" + query.lower() + "%" 
    cursor.execute("SELECT * FROM Students WHERE LOWER(id) LIKE %s OR LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s OR CAST(year_level AS CHAR) LIKE %s OR LOWER(gender) LIKE %s OR LOWER(coursecode) LIKE %s", (query, query, query, query, query, query))
    
    search_results = [{'id': row[0], 'first_name': row[1], 'last_name': row[2], 'year_level': row[3], 'gender': row[4], 'coursecode': row[5]} for row in cursor.fetchall()]

    conn.close()

    return render_template('searchStudent.html', search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True)
