# 🚀 CareerPilot

### Discover. Assess. Learn. Grow.

CareerPilot is an AI-powered personalized career and learning platform designed to help learners discover suitable career paths, assess their skills, identify skill gaps, follow personalized learning roadmaps, and track their learning progress.

The platform combines Python, Django, Django REST Framework, PostgreSQL, and AI-powered guidance to create a personalized learning experience.

---

## 📌 Overview

Traditional learning platforms often provide the same courses and learning paths to every learner.

CareerPilot aims to make learning more personalized by considering a learner's:

- 🎯 Career goals
- 🧠 Skills
- 📝 Assessment performance
- 📊 Strengths and weaknesses
- 📚 Learning progress

Based on this information, CareerPilot will provide personalized career guidance and learning recommendations.

---

## 🎯 Objectives

CareerPilot aims to:

- Help learners discover suitable career paths
- Assess technical and professional skills
- Identify strengths and skill gaps
- Generate personalized learning roadmaps
- Provide courses and learning resources
- Provide quizzes and practice activities
- Track learning progress
- Provide AI-powered guidance
- Generate certificates for eligible learners
- Provide a backend architecture that can support a future mobile application

---

# ✨ Features

## 🔐 Authentication

- User registration
- Email verification
- Secure password hashing
- Login with username or email
- Django session authentication
- Logout
- Password reset
- Google authentication
- GitHub authentication
- Role-based access

> Password reset and social authentication are planned features.

---

## 👤 Student Profile

Learners will be able to maintain:

- Full name
- Email
- Phone number
- Education
- Skills
- Career interests
- Career goals

---

## 🧭 Career Exploration

Learners will be able to:

- Browse career paths
- View career descriptions
- Explore required skills
- Understand career requirements
- Identify relevant skills

---

## 📝 Skill Assessment

CareerPilot will provide assessments to evaluate learner skills.

The assessment system will include:

- Assessments
- Questions
- Options
- Assessment attempts
- Answer submission
- Automatic scoring
- Skill-wise results

---

## 📊 Skill Gap Analysis

CareerPilot will compare a learner's current skills with the skills required for a selected career.

```text
Current Skills
      +
Career Requirements
      ↓
Skill Gap Analysis
      ↓
Skills to Improve

🗺️ Personalized Learning Roadmap
--------------------------------------
The platform will generate personalized learning roadmaps based on:
Career goals
Assessment results
Current skills
Skill gaps
Learning progress

Example:

Python
   ↓
Django
   ↓
REST APIs
   ↓
PostgreSQL
   ↓
Backend Project
   ↓
Backend Developer

📚 Courses & Learning
------------------------
CareerPilot will support:
Courses
Modules
Lessons
Learning resources
Quizzes
Practice activities
Progress tracking

🤖 AI-Powered Guidance
---------------------------
AI will be used to provide:
Career guidance
Personalized recommendations
Learning explanations
Skill improvement suggestions
AI tutoring
Learning assistance

Hybrid AI Approach
--------------------
CareerPilot will keep core business rules and objective scoring within the Django application.

AI will primarily be used for:
Explanations
Recommendations
Personalized guidance
Tutoring

🏆 Certificates
-----------------------
Eligible learners will receive certificates after completing the required learning activities and/or assessments.

Future certificate features may include:
Certificate generation
Certificate verification
Public certificate pages
QR-based verification

📱 Future Mobile Application
----------------------------------
CareerPilot will be designed with a future mobile application in mind.

The backend and REST API architecture will allow a future mobile application to communicate with the same backend without requiring the entire backend to be rebuilt.

🛠️ Technology Stack
____________________________________________________
| Layer	              |   Technology              |
|_______________________|___________________________|
| Programming Language  |   Python                  |
| Backend Framework	    |   Django                  |
| API Framework	    |   Django REST Framework   |
| Frontend	         |   HTML5, CSS3, JavaScript |
| Database	         |   PostgreSQL              |
|  AI	              |   LLM / AI API            |
| Version Control	    |    Git                    |
| Repository	         |    GitHub                 |
| IDE	              |    Visual Studio Code     |
______________________________________________________

🎨 UI & Design
----------------
CareerPilot uses a Dark Premium design system.

ColorPalette
____________________________________
| Purpose          |  Color         |
|-----------------------------------|
| Background	    |  #0F172A       |
| Cards /Secondary |  #1E293B       |
| Primary	         |  #8B5CF6       |
|  Accent	         |  #A78BFA       |
| Main Text        |  #F8FAFC       |
| Secondary Text   |  #CBD5E1       |
| Border	         |  #334155       |
|__________________|________________|

The design language will be applied consistently across:
Landing Page
Registration
Login
Dashboard
Career Paths
Assessments
Courses
Certificates
Student Profile
AI Tutor

🏗️ Project Architecture
-----------------------------
CareerPilot/
│
├── CareerPilot/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── core/
│   ├── views.py
│   └── ...
│
├── templates/
│   ├── base.html
│   ├── home.html
│   └── accounts/
│       ├── register.html
│       ├── login.html
│       ├── check_email.html
│       └── email_verification.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md

🔄 Authentication Flow
--------------------------
                    CareerPilot
                         │
                         ↓
                  User Registration
                         │
                         ↓
                    Create User
                         │
                         ↓
                  Email Verification
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
        Verification OK        Verification Failed
              │                     │
              ↓                     ↓
       Activate Account       Verification Error
              │
              ↓
             Login
              │
              ↓
       Username / Email
              +
           Password
              │
              ↓
     Django Authentication
              │
              ↓
       Create User Session
              │
              ↓
          Home Page

📂 Current Development Progress

Phase 0 — Project Foundation
----------------------
 Django project setup
 Existing deepti virtual environment configured
 PostgreSQL database configured
 Environment configuration
 accounts app created
 core app created
 Templates structure created
 Static files structure created
 Base template created
 Home page created
 Dark Premium UI established
 Git configured
 GitHub repository connected

Phase 1 — Authentication
----------------------
Completed

 Registration UI
 Registration form
 Password hashing
 Email verification model
 Email verification token
 Email verification flow
 Account activation
 Login UI
 Login with username
 Login with email
 Django session authentication
 Login testing

Remaining

 Dynamic authenticated navbar
 Logout
 Remember Me functionality
 Forgot Password
 Google authentication
 GitHub authentication

🗺️ Development Roadmap
-----------------------
Phase 0
Project Foundation
       ↓
Phase 1
Authentication
       ↓
Phase 2
Student Profile
       ↓
Phase 3
Career Catalog
       ↓
Phase 4
Skill Assessments
       ↓
Phase 5
Skill Gap Analysis
       ↓
Phase 6
Personalized Roadmap
       ↓
Phase 7
Courses & Learning
       ↓
Phase 8
AI Features
       ↓
Phase 9
Certificates
       ↓
Phase 10
REST APIs
       ↓
Future
Mobile Application

📋 Development Methodology
-----------------------
Every major feature will follow the same development process:

GUI / Visualization
        ↓
User Flow
        ↓
Database Design
        ↓
Django Concept
        ↓
Code
        ↓
Testing
        ↓
Git Commit
        ↓
GitHub

This approach keeps the project organized and makes every feature easier to understand, test, maintain, and extend.

🚀 Getting Started

Prerequisites
Make sure the following are installed:
Python 3.13+
Django 5.2+
PostgreSQL 18+
Git
Visual Studio Code

1. Clone the Repository
git clone https://github.com/beheradeeptimayee/CareerPilot.git

Then:
cd CareerPilot

2. Activate the Virtual Environment
CareerPilot currently uses the existing deepti virtual environment.
deepti\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the project root.

Example:

SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=careerpilot_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

⚠️ Never commit the .env file to GitHub.

5. Apply Database Migrations
python manage.py migrate

6. Start the Development Server
python manage.py runserver
Open the application:

http://127.0.0.1:8000/

🧪 Testing
-----------------------
Before committing a feature, run:

python manage.py check

Then test the feature manually through the browser.
Authentication Test

Registration
     ↓
Email Verification
     ↓
Account Activation
     ↓
Login
     ↓
Home Page

🔀 Git Workflow
------------------------
GitHub is used as the development checkpoint for CareerPilot.

After completing and testing a meaningful feature:

git status
Then:
git add .
Create a commit:
git commit -m "Describe the feature"

Push the changes:
git push
Example
git add .
git commit -m "Add login authentication and UI"
git push

🔐 Security
---------------
Sensitive information must never be committed to GitHub.

Examples include:
Secret keys
Database passwords
API keys
Email credentials
Other private configuration
These values are stored in .env.
The .env file is excluded from Git using .gitignore.

🔮 Future Enhancements
----------------------------
Future versions of CareerPilot may include:

📱 Native Android/iOS applications
🧠 Adaptive assessments
🤖 AI-generated study plans
📝 AI-generated practice questions
🎙️ Voice-based AI Tutor
🔔 Notifications
🎮 Gamification
📊 Advanced analytics
📄 Resume and portfolio builder
💼 Interview preparation
🔗 External learning providers
🔐 QR-based certificate verification
🧠 Advanced recommendation models
📈 Current Project Status
🟢 Status: In Development

Current Milestone
---------------------
Authentication and account verification foundation completed.

Current working flow:

Home
 ↓
Registration
 ↓
Email Verification
 ↓
Account Activation
 ↓
Login
 ↓
Django Session
 ↓
Home

Next Milestone
----------------
Dynamic Navbar
      ↓
Logout
      ↓
Student Profile
      ↓
Dashboard

👩‍💻 Developer
--------------
Deepti Mayee Behera

B.Tech — Computer Science & Engineering

CareerPilot is being developed as a portfolio and learning project with a focus on:

Python
Django
PostgreSQL
REST APIs
Backend Development
AI Integration
Personalized Learning Systems

⭐ CareerPilot
Discover. Assess. Learn. Grow.
Built with ❤️ using Python + Django + PostgreSQL

📄 License

This project is currently developed for educational, portfolio, and learning purposes.




