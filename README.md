# Student Task Tracker

A web-based task management application built using **Python, Flask, SQLite, HTML, CSS, and JavaScript**. Student Task Tracker helps students organize their academic tasks, monitor progress, and manage deadlines through a simple dashboard.

This project is developed as part of a **Software Engineering and Agile Project Management** demonstration.

## Features

- **User Registration and Login** — Create an account and securely log in.
- **Personalized Dashboard** — View task statistics and get an overview of your work.
- **Task Management** — Add, edit, view, and delete tasks.
- **Task Status Tracking** — Track tasks as Todo, In Progress, or Done.
- **Priority Management** — Organize tasks by priority, including high-priority tasks.
- **Due Dates** — Set deadlines to help manage time effectively.
- **Search and Filtering** — Find tasks and filter them by status.
- **User Data Isolation** — Each user can access their own tasks.
- **Password Security** — Passwords are hashed rather than stored as plain text.
- **Responsive Interface** — Use the application through a browser on different screen sizes.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Version Control | Git and GitHub |

## Project Structure

```text
Student_Task_Tracker/
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    ├── index.html
    ├── login.html
    └── register.html
```

The SQLite database is created locally by the application and is not included in the Git repository.

## Installation and Setup

### Prerequisites

- Python 3 installed
- Git installed
- A web browser

### 1. Clone the repository

```bash
git clone https://github.com/sanikamc/SE-Agile-Demonstration.git
cd SE-Agile-Demonstration
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the local URL displayed in the terminal. For a typical Flask development setup, this is:

`http://127.0.0.1:5000`

If the application uses a different port in your configuration, use the URL shown in your terminal.

## How to Use

1. Register a new account.
2. Log in using your credentials.
3. Open the dashboard to view your task statistics.
4. Add tasks with the relevant details, priority, status, and due date.
5. Update task status as you make progress.
6. Search, filter, edit, or delete tasks as needed.
7. Log out when you finish.

## Agile Project Management

This project demonstrates the application of software engineering and Agile project management principles.

- **Requirements:** Identify the needs of student users and define functional requirements.
- **Product Backlog:** Organize project requirements and development tasks.
- **Task Breakdown:** Divide development into manageable pieces of work.
- **Incremental Development:** Build and refine the application feature by feature.
- **Testing:** Verify important workflows such as authentication and task management.
- **Version Control:** Use Git and GitHub to track code changes.

## Future Enhancements

Potential improvements include:

- Task reminders and notifications
- Calendar-based task visualization
- Exporting task reports
- Enhanced dashboard analytics
- Automated unit and integration tests

## Author

**Sanika M. C.**

GitHub: [@sanikamc](https://github.com/sanikamc)

## Repository

[SE-Agile-Demonstration](https://github.com/sanikamc/SE-Agile-Demonstration)

---

*Student Task Tracker — Organize tasks, track progress, and stay productive.*
