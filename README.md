# Online Examination Management System

## Project Overview

The Online Examination Management System is a web-based application developed using Python Flask and SQLite. It provides a platform for students to register, log in, select an available course, attend an online multiple-choice examination, and view their latest examination result. The application also includes an administrator section for viewing registered students and examination results.

## Project Objectives

- Provide a web-based platform for online examinations.
- Allow students to register and log in.
- Allow students to select an available course: B.Sc., BBA, or BCA.
- Display examination instructions before the examination.
- Evaluate submitted answers and calculate scores automatically.
- Assign a grade based on the percentage scored.
- Allow administrators to view student details and examination results.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite

## Main Modules and Features

### Student Module

- Student registration with name, email, password, age, gender, and mobile number.
- Password format validation during registration.
- Student login and logout.
- Student dashboard and profile page.
- Examination instructions page.
- Course selection for B.Sc., BBA, and BCA.
- Separate examination pages for the available courses.
- Automatic evaluation of 10 submitted questions.
- Result storage and latest-result viewing.
- Help and contact pages.

### Admin Module

- Admin registration and login.
- Admin dashboard.
- View registered student records.
- View stored examination results.
- Admin logout.

## Examination and Grading

The application checks 10 submitted questions. Each answer submitted with the expected value is counted as one correct answer. The score is saved in the database, along with the selected course and grade.

| Percentage | Grade |
|---|---|
| 80% and above | A |
| 60% to below 80% | B |
| Below 60% | C |

## Database

The project uses an SQLite database file named `database.db`. The application creates and uses the following tables:

- **students:** Student registration and profile information.
- **results:** Student email, course, score, total questions, and grade.
- **admin:** Administrator username and password.

## Project Folder Structure

```text
online examination/
├── app.py
├── database.db
├── static/
│   ├── img.jpg
│   ├── image1.jpeg
│   ├── dash.jpg
│   └── QR-Code.png
└── templates/
    ├── admin.html
    ├── admin_dashboard.html
    ├── admin_login.html
    ├── admin_register.html
    ├── contact.html
    ├── dashboard.html
    ├── exam.html
    ├── exam_bba.html
    ├── exam_bca.html
    ├── exam_bsc.html
    ├── help.html
    ├── instructions.html
    ├── login.html
    ├── profile.html
    ├── register.html
    └── result.html
```

## How to Run the Project Locally

### 1. Install Python

Install Python 3 on your computer. During installation on Windows, select **Add Python to PATH** if that option is shown.

### 2. Open the project folder

Open Command Prompt or a terminal and change to the folder that contains `app.py`.

### 3. Install Flask

Run:

```bash
python -m pip install Flask
```

### 4. Start the application

Run:

```bash
python app.py
```

### 5. Open the application

Open a web browser and visit:

```text
http://127.0.0.1:5000/
```

The home route redirects to the student login page.

## Important Notes

- This is an academic project intended to run locally for demonstration and learning.
- The application uses a local SQLite database named `database.db`.
- Do not upload real student personal information, passwords, or other confidential records to a public repository. If the database contains real or sensitive records, remove it from the public upload and provide an empty/sample database instead.
- Before deploying this application publicly, replace the hardcoded Flask secret key, use secure password hashing, and review authentication and application security.

## Developed By

**Harshada Namdeo Jadhav**  
M.Sc. Computer Science  

**Project:** Online Examination Management System
