import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

def get_db_connection():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "tododb"),
        cursorclass=DictCursor,
        connect_timeout=5,
        autocommit=True,
    )

@app.get("/")
def index():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, completed, created_at FROM tasks ORDER BY created_at DESC"
                )
                tasks = cursor.fetchall()
    except Exception:
        app.logger.exception("Could not load tasks from database")
        flash("The database is temporarily unavailable. Please try again.", "error")
        tasks = []
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        progress=round(completed / total * 100) if total else 0,
    )

@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Please enter a task title.", "error")
        return redirect(url_for("index"))
    if len(title) > 255:
        flash("Task title must be 255 characters or fewer.", "error")
        return redirect(url_for("index"))
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        flash("Task added successfully.", "success")
    except Exception:
        app.logger.exception("Could not add task")
        flash("Could not save your task. Check the database connection.", "error")
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE tasks SET completed = NOT completed WHERE id = %s",
                    (task_id,),
                )
        flash("Task status updated.", "success")
    except Exception:
        app.logger.exception("Could not update task")
        flash("Could not update this task.", "error")
    return redirect(url_for("index"))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        flash("Task deleted.", "success")
    except Exception:
        app.logger.exception("Could not delete task")
        flash("Could not delete this task.", "error")
    return redirect(url_for("index"))

@app.get("/health")
def health():
    return jsonify(status="healthy", application="TaskNova"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
