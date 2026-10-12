
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CareerPilot.settings")
django.setup()

from django.db import transaction
from assessments.models import Assessment, Question, QuestionOption
from careers.models import Skill

questions_data = [
    ("HTML", "Which HTML element creates a hyperlink?",
     [("<a>", True), ("<link>", False), ("<href>", False), ("<url>", False)]),

    ("CSS", "Which CSS property controls space inside an element's border?",
     [("margin", False), ("padding", True), ("border-spacing", False), ("outline", False)]),

    ("JavaScript", "Which keyword declares a block-scoped variable that can be reassigned?",
     [("const", False), ("let", True), ("static", False), ("define", False)]),

    ("Python", "Which Python data type stores key-value pairs?",
     [("list", False), ("tuple", False), ("dict", True), ("set", False)]),

    ("Django", "What is the primary purpose of Django's ORM?",
     [("To style HTML pages", False),
      ("To interact with database records using Python objects", True),
      ("To compile JavaScript", False),
      ("To configure web browsers", False)]),

    ("REST APIs", "Which HTTP method is commonly used to retrieve a resource?",
     [("POST", False), ("DELETE", False), ("GET", True), ("PATCH", False)]),

    ("SQL", "Which SQL clause filters rows before grouping?",
     [("ORDER BY", False), ("HAVING", False), ("WHERE", True), ("GROUP BY", False)]),

    ("PostgreSQL", "Which SQL command retrieves rows from a table?",
     [("FETCH TABLE", False), ("SELECT", True), ("READ TABLE", False), ("OPEN TABLE", False)]),

    ("MySQL", "Which SQL command adds a new row to a table?",
     [("UPDATE", False), ("ALTER", False), ("INSERT", True), ("CREATE", False)]),

    ("Database Management", "What is the primary purpose of a primary key?",
     [("Uniquely identify each row in a table", True),
      ("Sort all rows alphabetically", False),
      ("Encrypt every column", False),
      ("Duplicate records", False)]),
]

assessment = Assessment.objects.get(career__slug="full-stack-developer")

if Question.objects.filter(assessment=assessment).exists():
    print("Questions already exist. No changes made.")
else:
    with transaction.atomic():
        for index, (skill_name, text, options) in enumerate(questions_data, start=1):
            skill = Skill.objects.get(name=skill_name)

            question = Question.objects.create(
                assessment=assessment,
                skill=skill,
                question_text=text,
                question_type="MCQ",
                difficulty="EASY" if index <= 4 else "MEDIUM",
                marks=1,
                order=index,
                source="MANUAL",
                ai_generated=False,
            )

            for option_text, is_correct in options:
                QuestionOption.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=is_correct,
                )

    print(f"Successfully created {len(questions_data)} questions.")
