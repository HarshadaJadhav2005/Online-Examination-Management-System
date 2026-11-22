from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = "online_exam_secret"

DB_NAME = "database.db"

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row
    return con

# ---------------- CREATE TABLES ----------------
def create_tables():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        age INTEGER,
        gender TEXT,
        mobile TEXT
    )
    """)

    # Check if 'results' table exists and has 'course' column
    cur.execute("PRAGMA table_info(results)")
    columns = [row['name'] for row in cur.fetchall()]
    if 'course' not in columns:
        # Drop old table if exists
        cur.execute("DROP TABLE IF EXISTS results")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        course TEXT,
        score INTEGER,
        total INTEGER,
        grade TEXT
    )
     """)
    
    
    
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
     """)






    con.commit()
    con.close()

create_tables()

#------------------admin register route-------------


@app.route('/admin_register', methods=['GET','POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO admin (username,password) VALUES (?,?)",
            (username,password)
        )
        con.commit()
        con.close()

        return redirect('/admin_login')

    return render_template("admin_register.html")


#----------------admin login ----------------

@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username,password)
        )
        admin = cur.fetchone()
        con.close()

        if admin:
            session['admin'] = username
            return redirect('/admin_dashboard')

        return "Invalid Login"

    return render_template("admin_login.html")

#------------------admin dashboard----------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin_login')

    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    cur.execute("SELECT * FROM results")
    results = cur.fetchall()

    con.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        results=results
    )

#-------------------admin logout ----------------
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin_login')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()
        con.close()

        if user:
            session['student_email'] = user['email']
            session['student_name'] = user['name']
            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template("login.html")


# ✅ -------- LOGIN FIX (IMPORTANT) --------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        mobile = request.form['mobile']

        # Password validation
        pattern = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$'

        if not re.match(pattern, password):
            return "Password must contain 1 Capital letter, 1 Number, 1 Special character and be at least 8 characters."

        con = get_db()
        cur = con.cursor()

        try:
            cur.execute("""
            INSERT INTO students (name,email,password,age,gender,mobile)
            VALUES (?,?,?,?,?,?)
            """,(name,email,password,age,gender,mobile))

            con.commit()
            con.close()
            return redirect('/login')

        except:
            con.close()
            return "Email already exists"

    return render_template("register.html")






# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("dashboard.html", name=session['student_name'])

# ---------------- PROFILE ----------------
@app.route('/profile')
def profile():
    if 'student_email' not in session:
        return redirect('/')

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM students WHERE email=?",
        (session['student_email'],)
    )
    student = cur.fetchone()
    con.close()

    return render_template("profile.html", student=student)

# ---------------- INSTRUCTIONS ----------------
@app.route('/instructions')
def instructions():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("instructions.html")

# ---------------- COURSE SELECTION ----------------
@app.route('/select_course', methods=['POST'])
def select_course():
    course = request.form.get('course')
    if not course:
        return "Please select a course"
    
    session['course'] = course

    # Redirect to course-specific HTML
    if course == "B.Sc":
        return redirect('/exam/bsc')
    elif course == "BBA":
        return redirect('/exam/bba')
    elif course == "BCA":
        return redirect('/exam/bca')
    else:
        return "Exam not available for this course"

# ---------------- EXAM ROUTES ----------------
@app.route('/exam/bsc')
def exam_bsc():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("exam_bsc.html")

@app.route('/exam/bba')
def exam_bba():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("exam_bba.html")

@app.route('/exam/bca')
def exam_bca():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("exam_bca.html")

# ---------------- RESULT ----------------
@app.route('/result', methods=['POST'])
def result():
    if 'student_email' not in session:
        return redirect('/')

    score = 0
    total = 10  # 10 questions per exam

    for i in range(1, 11):
        if request.form.get(f'q{i}') == 'correct':
            score += 1

    percentage = (score / total) * 100

    if percentage >= 80:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    else:
        grade = "C"

    con = get_db()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO results (student_email, course, score, total, grade)
        VALUES (?, ?, ?, ?, ?)
    """, (session['student_email'], session.get('course'), score, total, grade))
    con.commit()
    con.close()

    flash("✅ Exam submitted successfully!", "success")
    return redirect('/dashboard')

# ---------------- VIEW RESULT ----------------
@app.route('/view_result')
def view_result():
    if 'student_email' not in session:
        return redirect('/')

    con = get_db()
    cur = con.cursor()
    cur.execute("""
    SELECT * FROM results
    WHERE student_email=?
    ORDER BY id DESC LIMIT 1
    """,(session['student_email'],))
    result = cur.fetchone()
    con.close()

    if result:
        return render_template(
            "result.html",
            name=session['student_name'],
            score=result['score'],
            total=result['total'],
            grade=result['grade']
        )
    return "No result found"

# ---------------- HELP & CONTACT ----------------
@app.route('/help')
def help_page():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("help.html")
# ---------------- ADMIN DASHBOARD ----------------
#@app.route('/admin')
#def admin_dashboard():
#    con = get_db()
#    cur = con.cursor()
#    cur.execute("SELECT * FROM students")
#    students = cur.fetchall()
#    con.close()

#    return render_template("admin.html", students=students)


@app.route('/contact')
def contact_page():
    if 'student_name' not in session:
        return redirect('/')
    return render_template("contact.html")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)

