# 🚀 CareerPilot

### Discover. Assess. Learn. Grow.

CareerPilot is an AI-powered personalized career and learning platform designed to help learners understand their skills, explore suitable career paths, identify skill gaps, follow personalized learning roadmaps, and track their progress.

The platform combines a Django-based web application, REST APIs, PostgreSQL, and AI-powered guidance to create a personalized learning experience.

---

## 📌 Project Overview

Traditional learning platforms often provide the same courses and learning paths to every learner.

CareerPilot aims to make learning more personalized.

The platform analyzes a learner's:

- Career interests
- Skills
- Assessment performance
- Strengths
- Weaknesses
- Learning progress
- Career goals

Based on this information, CareerPilot provides personalized career guidance and learning recommendations.

---

## 🎯 Main Objectives

CareerPilot aims to:

- Help learners discover suitable career paths
- Assess technical and professional skills
- Identify strengths and skill gaps
- Generate personalized learning roadmaps
- Provide courses and learning resources
- Provide quizzes and practice activities
- Track learning progress
- Provide AI-powered guidance
- Generate certificates for eligible completed learning paths
- Provide a foundation for a future mobile application

---

# ✨ Features

## 👤 User Authentication

CareerPilot provides a secure authentication system including:

- User registration
- Email verification
- Login
- Logout
- Password reset
- Secure password handling
- User authentication
- Role-based access

### Current Authentication Flow

```text
Registration
     ↓
Create Account
     ↓
Email Verification
     ↓
Activate Account
     ↓
Login
     ↓
Django Authentication
     ↓
Create Session
     ↓
Home Page


👨‍🎓 Student Profile
---------------------
Learners will be able to maintain information such as:
Full name
Email
Phone number
Career interests
Education
Skills
Career goals

🧭 Career Exploration
------------------------------
Learners will be able to:
Explore different career paths
View career descriptions
Understand required skills
Identify skills required for a career
Compare their current skills with career requirements
Identify areas that need improvement

📝 Skill Assessment
------------------------
CareerPilot will provide assessments to evaluate learner skills.
The assessment system will include:
Assessments
Questions
Options
Assessment attempts
Submitted answers
Automatic scoring
Skill-wise results

📊 Skill Gap Analysis
--------------------------
The platform will analyze assessment results and career requirements to identify:
Existing skills
Strong skills
Weak skills
Missing skills
Skills required for a selected career
This information will be used to create a personalized learning path.


🗺️ Personalized Learning Roadmap
------------------------------------
CareerPilot will generate personalized learning roadmaps based on:
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

📚 Courses and Learning
--------------------------
The learning system will support:
Courses
Modules
Lessons
Learning resources
Quizzes
Practice activities
Progress tracking
Learners will be able to follow their personalized roadmap and track their learning progress.

🤖 AI-Powered Guidance
-----------------------
CareerPilot will integrate AI to provide personalized assistance.
Possible AI features include:
Personalized recommendations
Career guidance
Learning explanations
Skill improvement suggestions
AI tutoring
Learning assistance
Hybrid AI Approach

Core business rules and objective scoring will be handled by the Django application.
AI will primarily be used for:
Explanations
Recommendations
Personalized guidance
Tutoring
This helps keep important application logic deterministic while using AI where personalization is useful.

🏆 Certificates
-------------------
CareerPilot will provide certificates to learners who successfully complete eligible courses and/or assessments.

Future certificate features may include:
Certificate generation
Certificate verification
Public certificate pages
QR-based verification

📱 Future Mobile Application
----------------------------------
The backend and REST API architecture will be designed with future mobile development in mind.

The goal is to allow a future mobile application to communicate with the same backend through APIs without rebuilding the entire application.

🛠️ Technology Stack
---------------------
Backend
Python
Django
Django REST Framework
Frontend
HTML5
CSS3
JavaScript
Database
PostgreSQL
AI
LLM / AI API integration
Development Tools
Git
GitHub
Visual Studio Code

🏗️ Project Architecture
----------------------------
CareerPilot follows a Django-based architecture.

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

🎨 UI Design
------------------
CareerPilot uses a Dark Premium visual theme.

Color Palette
Purpose	Color
Background	#0F172A
Secondary Background	#1E293B
Primary	#8B5CF6
Accent	#A78BFA
Main Text	#F8FAFC
Secondary Text	#CBD5E1
Border	#334155

The Dark Premium design will be used consistently throughout the application.

Planned UI areas include:

Landing page
Registration
Login
Dashboard
Career paths
Assessments
Courses
Certificates
Student profile
AI Tutor

🔄 Development Methodology
---------------------------
Each major CareerPilot feature will follow this development process:

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

This approach helps make the project easier to understand, develop, test, maintain, and extend.

🗂️ Development Progress
-------------------------
Phase 0 — Project Foundation
--------------------------------
 Django project created
 Existing deepti virtual environment configured
 PostgreSQL configured
 Environment variables configured
 accounts app created
 core app created
 Templates structure created
 Static files structure created
 Dark Premium UI established
 Base template created
 Home page created
 Git initialized
 GitHub repository connected

Phase 1 — Authentication
-------------------------------
COMPLETED:
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

**Pending**
---------
 Dynamic authenticated navbar
 Logout
 Forgot password
 Google authentication
 GitHub authentication
 Remember Me functionality

📊 Planned Development Phases
Phase 2 — Student Profile
-----------------------
 Student profile model
 Profile creation
 Profile editing
 Career interests
 Skills
 Education details
 Career goals

Phase 3 — Career Catalog
---------------------
 Career model
 Career categories
 Skill catalog
 Career-skill mapping
 Career listing
 Career detail page

Phase 4 — Assessments
---------------------
 Assessment model
 Questions
 Options
 Assessment attempts
 Answer submission
 Automatic scoring
 Skill-wise results
 Skill gap analysis

Phase 5 — Personalized Roadmap
------------------------------
 Roadmap model
 Roadmap generation
 Skill-based learning paths
 Career-based recommendations
 Roadmap progress tracking

Phase 6 — Courses and Learning
--------------------------------
 Courses
 Modules
 Lessons
 Learning resources
 Quizzes
 Practice activities
 Progress tracking

Phase 7 — AI Features
------------------
 AI Tutor
 AI learning explanations
 Personalized recommendations
 AI career guidance
 AI learning assistance
 AI-powered study support

Phase 8 — Certificates
------------------------
 Certificate model
 Certificate eligibility
 Certificate generation
 Certificate dashboard
 Certificate verification
 QR-based verification

Phase 9 — REST API
--------------------
 API architecture
 Authentication APIs
 Career APIs
 Assessment APIs
 Course APIs
 Progress APIs
 Certificate APIs

Phase 10 — Future Mobile Architecture
--------------------------
 Mobile-ready API architecture
 Mobile authentication
 Mobile dashboard
 Mobile career exploration
 Mobile assessments
 Mobile learning experience
 Mobile certificates

🚀 Getting Started
Prerequisites
---------------
Make sure the following are installed:

Python
PostgreSQL
Git
Visual Studio Code

CareerPilot currently uses:

Python 3.13.1
Django 5.2.5
PostgreSQL 18.4
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

Never commit the .env file to GitHub.

5. Run Database Migrations
python manage.py migrate
6. Run the Development Server
python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/
🧪 Testing

Before committing a feature, run:

python manage.py check

Then test the feature manually through the browser.

For example, for authentication:

Registration
     ↓
Email Verification
     ↓
Login
     ↓
Home Page

After successful testing, create a Git checkpoint.

🔀 Git Workflow

GitHub is used as the development checkpoint for CareerPilot.

After completing and testing a meaningful feature:

git status

Then:

git add .

Create a commit:

git commit -m "Describe the feature"

Push to GitHub:

git push

Example:

git add .
git commit -m "Add login authentication and UI"
git push
🔐 Security Notes

The project uses environment variables for sensitive configuration.

The following should never be committed to GitHub:

Secret keys
Database passwords
API keys
Email credentials
Other private configuration

The .env file is therefore included in .gitignore.

🔮 Future Enhancements

Future versions of CareerPilot may include:

Native Android/iOS applications
Adaptive assessments
AI-generated study plans
AI-generated practice questions
Voice-based AI Tutor
Notifications
Gamification
Advanced analytics
Resume and portfolio building
Interview preparation
External learning providers
QR-based certificate verification
Advanced recommendation models
📌 Current Project Status

CareerPilot is currently under active development.

Current milestone

Authentication and account verification foundation completed.

Current working flow:

CareerPilot Home
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
Home Page
Next milestone
Dynamic Navbar
       ↓
Logout
       ↓
Student Profile
       ↓
Dashboard
👩‍💻 Developer

Deepti Mayee Behera

Bachelor of Technology — Computer Science and Engineering

CareerPilot is being developed as a full-stack Django project with a focus on:

Backend development
Django
PostgreSQL
REST APIs
Authentication
AI integration
Personalized learning systems
📄 License

This project is currently developed for educational, portfolio, and learning purposes.


### Where to save it

Your final structure should be:

```text
CareerPilot/
├── README.md          ← THIS FILE
├── manage.py
├── requirements.txt
├── .gitignore
├── .env
├── CareerPilot/
├── accounts/
├── core/
├── templates/
└── static/
