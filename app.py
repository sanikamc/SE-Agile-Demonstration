
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from functools import wraps
from database import (
    init_db,
    create_user,
    get_user_by_email,
    verify_password,
    get_all_tasks,
    add_task,
    get_task,
    update_task,
    delete_task,
)

app = Flask(__name__)

# Replace this with a long, random secret before deployment.
app.config["SECRET_KEY"] = "replace-this-with-a-long-random-secret-key"

init_db()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("index"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("register.html")

        if get_user_by_email(email):
            flash("An account with this email already exists.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except Exception:
            flash("Unable to create account. Please try again.", "error")
            return render_template("register.html")

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if not verify_password(user, password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def index():
    tasks = get_all_tasks(session["user_id"])
    return render_template(
        "index.html",
        tasks=tasks,
        user_name=session.get("user_name", "Student")
    )


@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title", "").strip()

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("index"))

    description = request.form.get("description", "").strip()
    subject = request.form.get("subject", "").strip()
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "")

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    add_task(
        title, description, subject, priority, due_date,
        session["user_id"]
    )
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["POST"])
@login_required
def edit(task_id):
    task = get_task(task_id, session["user_id"])

    if task is None:
        flash("Task not found.", "error")
        return redirect(url_for("index"))

    title = request.form.get("title", "").strip()

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("index"))

    description = request.form.get("description", "").strip()
    subject = request.form.get("subject", "").strip()
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "")
    status = request.form.get("status", "Todo")

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    if status not in ["Todo", "In Progress", "Done", "Completed"]:
        status = "Todo"

    if status == "Completed":
        status = "Done"

    update_task(
        task_id, title, description, subject, priority,
        due_date, status, session["user_id"]
    )
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):
    delete_task(task_id, session["user_id"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
