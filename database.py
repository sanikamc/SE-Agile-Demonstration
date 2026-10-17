
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

# Always use the database inside this project's folder.
DATABASE = Path(__file__).resolve().parent / "student_tasks.db"


def get_connection():
    conn = sqlite3.connect(str(DATABASE))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                subject TEXT DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Medium',
                due_date TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Todo',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Add user_id to an existing database without deleting tasks.
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(tasks)").fetchall()
        }

        if "user_id" not in columns:
            conn.execute(
                "ALTER TABLE tasks ADD COLUMN user_id INTEGER REFERENCES users(id)"
            )


def create_user(name, email, password):
    email = email.strip().lower()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name.strip(), email, generate_password_hash(password))
        )

        user = conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        user_count = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        # Assign old, unowned tasks to the first registered user only.
        if user_count == 1 and user is not None:
            conn.execute(
                "UPDATE tasks SET user_id = ? WHERE user_id IS NULL",
                (user["id"],)
            )


def get_user_by_email(email):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),)
        ).fetchone()


def verify_password(user, password):
    return user is not None and check_password_hash(
        user["password_hash"], password
    )


def get_all_tasks(user_id=None):
    with get_connection() as conn:
        if user_id is None:
            return conn.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            ).fetchall()

        return conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        ).fetchall()


def add_task(title, description, subject, priority, due_date, user_id=None):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO tasks
                (title, description, subject, priority, due_date, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, description, subject, priority, due_date, user_id)
        )


def get_task(task_id, user_id=None):
    with get_connection() as conn:
        if user_id is None:
            return conn.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,)
            ).fetchone()

        return conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()


def update_task(
    task_id, title, description, subject,
    priority, due_date, status, user_id=None
):
    with get_connection() as conn:
        if user_id is None:
            conn.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, subject = ?,
                    priority = ?, due_date = ?, status = ?
                WHERE id = ?
                """,
                (
                    title, description, subject,
                    priority, due_date, status, task_id
                )
            )
        else:
            conn.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, subject = ?,
                    priority = ?, due_date = ?, status = ?
                WHERE id = ? AND user_id = ?
                """,
                (
                    title, description, subject, priority,
                    due_date, status, task_id, user_id
                )
            )


def delete_task(task_id, user_id=None):
    with get_connection() as conn:
        if user_id is None:
            conn.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )
        else:
            conn.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
