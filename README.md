# Online Student Course Registration System

## Project Overview
The Online Student Course Registration System is a web-based application developed using Python Flask and SQLite. It allows students to register, explore available courses, enroll in courses, view their registered courses, and drop courses through a simple and user-friendly interface.

## Features
- Student registration using name and email.
- Display available courses.
- Search courses by course name or instructor.
- Enroll in available courses.
- Prevent duplicate student registrations.
- Prevent duplicate course enrollments.
- View registered courses.
- Drop registered courses.
- Store student, course, and enrollment information using SQLite.

## Technologies Used
- **Frontend:** HTML, CSS
- **Backend:** Python, Flask
- **Database:** SQLite
- **Version Control:** Git
- **Remote Repository:** GitHub

## Project Structure

```text
StudentCourseRegistration/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── courses.db
│
├── templates/
│   ├── index.html
│   ├── courses.html
│   └── my_courses.html
│
├── static/
│   └── style.css
│
└── venv/
```

*Note: `courses.db` and `venv/` are generated locally and excluded from GitHub using `.gitignore`.*

## Installation and Execution

1. Clone the repository:

```bash
git clone https://github.com/ValliYanamadala/StudentCourseRegistration.git
```

2. Navigate to the project directory:

```bash
cd StudentCourseRegistration
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Run the Flask application:

```bash
python3 app.py
```

7. Open the application in your browser:

```text
http://127.0.0.1:5001
```

## Git and GitHub Workflow Demonstrated

The following Git operations were performed during development:

1. Repository initialization using `git init`.
2. File tracking using `git add`.
3. Staging and committing project changes.
4. Creating and switching between branches.
5. Developing features in separate branches.
6. Merging feature branches into the main branch.
7. Connecting a remote GitHub repository.
8. Pushing local commits to GitHub.
9. Creating and merging Pull Requests.
10. Pulling remote changes into the local repository.
11. Deleting merged local and remote branches.

## Repository

GitHub: https://github.com/ValliYanamadala/StudentCourseRegistration

## Conclusion

The project demonstrates the development of a basic web-based student course registration system using Flask and SQLite, along with practical implementation of Git and GitHub version control workflows, including branching, merging, remote repository management, and collaborative development.