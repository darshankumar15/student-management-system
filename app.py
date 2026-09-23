import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "student-management-demo-key")

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                roll_no VARCHAR(30) UNIQUE NOT NULL,
                department VARCHAR(50) NOT NULL,
                email VARCHAR(120),
                marks INTEGER NOT NULL CHECK (marks BETWEEN 0 AND 100)
            )
        """)
        conn.commit()

@app.route("/")
def index():
    with get_conn() as conn:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"].strip()
        roll_no = request.form["roll_no"].strip()
        department = request.form["department"].strip()
        email = request.form["email"].strip()
        marks = request.form["marks"].strip()

        try:
            marks = int(marks)
            with get_conn() as conn:
                conn.execute("""
                    INSERT INTO students (name, roll_no, department, email, marks)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, roll_no, department, email, marks))
                conn.commit()
            flash("Student added successfully.", "success")
            return redirect(url_for("index"))
        except ValueError:
            flash("Marks must be a number from 0 to 100.", "error")
        except Exception as e:
            if "unique" in str(e).lower():
                flash("Roll number already exists.", "error")
            else:
                flash("Unable to add student. Check the entered data.", "error")

    return render_template("form.html", student=None, title="Add Student")

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_conn() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id = %s", (student_id,)
        ).fetchone()

    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        try:
            marks = int(request.form["marks"])
            with get_conn() as conn:
                conn.execute("""
                    UPDATE students
                    SET name=%s, roll_no=%s, department=%s, email=%s, marks=%s
                    WHERE id=%s
                """, (
                    request.form["name"].strip(),
                    request.form["roll_no"].strip(),
                    request.form["department"].strip(),
                    request.form["email"].strip(),
                    marks,
                    student_id
                ))
                conn.commit()
            flash("Student updated successfully.", "success")
            return redirect(url_for("index"))
        except Exception:
            flash("Unable to update student. Check the entered data.", "error")

    return render_template("form.html", student=student, title="Edit Student")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Initializes the table when run locally.
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
