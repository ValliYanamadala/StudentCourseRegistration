
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "student_course_secret"

DATABASE = "courses.db"


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT NOT NULL,
            duration TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            UNIQUE(student_id, course_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM courses"
    ).fetchone()[0]

    if count == 0:
        sample_courses = [
            ("Python Programming", "Dr. Sharma", "8 Weeks"),
            ("Web Development", "Prof. Kumar", "10 Weeks"),
            ("Data Structures", "Dr. Reddy", "12 Weeks"),
            ("Machine Learning", "Prof. Priya", "10 Weeks"),
            ("Database Management", "Dr. Rao", "8 Weeks")
        ]

        conn.executemany("""
            INSERT INTO courses
            (course_name, instructor, duration)
            VALUES (?, ?, ?)
        """, sample_courses)

    conn.commit()
    conn.close()


# Home page and student registration
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO students (name, email) VALUES (?, ?)",
                (name, email)
            )
            conn.commit()

            student = conn.execute(
                "SELECT * FROM students WHERE email = ?",
                (email,)
            ).fetchone()

            student_id = student["id"]

            flash("Student registered successfully!")

            return redirect(url_for(
                "courses", student_id=student_id
            ))

        except sqlite3.IntegrityError:
            flash("This email is already registered.")

        finally:
            conn.close()

    return render_template("index.html")


# Display and search available courses
@app.route("/courses/<int:student_id>")
def courses(student_id):

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        return "Student not found", 404

    search_term = request.args.get("search", "").strip()

    if search_term:
        all_courses = conn.execute("""
            SELECT * FROM courses
            WHERE course_name LIKE ? OR instructor LIKE ?
        """, (
            f"%{search_term}%",
            f"%{search_term}%"
        )).fetchall()

    else:
        all_courses = conn.execute(
            "SELECT * FROM courses"
        ).fetchall()

    enrolled = conn.execute(
        "SELECT course_id FROM enrollments WHERE student_id = ?",
        (student_id,)
    ).fetchall()

    enrolled_ids = [row["course_id"] for row in enrolled]

    conn.close()

    return render_template(
        "courses.html",
        student=student,
        courses=all_courses,
        enrolled_ids=enrolled_ids,
        search_term=search_term
    )


# Enroll in a course
@app.route("/enroll/<int:student_id>/<int:course_id>", methods=["POST"])
def enroll(student_id, course_id):

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))

        conn.commit()
        flash("Successfully enrolled in the course!")

    except sqlite3.IntegrityError:
        flash("Already enrolled or invalid course/student.")

    finally:
        conn.close()

    return redirect(url_for("courses", student_id=student_id))


# View registered courses
@app.route("/my-courses/<int:student_id>")
def my_courses(student_id):

    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        return "Student not found", 404

    registered_courses = conn.execute("""
        SELECT courses.*, enrollments.id AS enrollment_id
        FROM enrollments
        JOIN courses ON courses.id = enrollments.course_id
        WHERE enrollments.student_id = ?
    """, (student_id,)).fetchall()

    conn.close()

    return render_template(
        "my_courses.html",
        student=student,
        courses=registered_courses
    )


# Drop a registered course
@app.route("/drop/<int:student_id>/<int:course_id>", methods=["POST"])
def drop_course(student_id, course_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM enrollments
        WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))

    conn.commit()
    conn.close()

    flash("Course registration removed.")

    return redirect(url_for(
        "my_courses", student_id=student_id
    ))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
