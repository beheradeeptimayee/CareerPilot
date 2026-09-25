from django.db import models

# Create your models here.
from careers.models import Career,Skill
from django.contrib.auth.models import User

class Assessment(models.Model):

    career = models.ForeignKey(Career,on_delete=models.CASCADE,related_name='assessments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AssessmentBlueprint(models.Model):

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('READY', 'Ready'),
        ('USED', 'Used'),
    ]

    assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE, related_name='blueprints')
    version = models.PositiveIntegerField(default=1)
    total_questions = models.PositiveIntegerField(default=20)
    duration_minutes = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.assessment.title} - Version {self.version}'


class BlueprintSkill(models.Model):

    blueprint = models.ForeignKey(AssessmentBlueprint,on_delete=models.CASCADE,related_name='blueprint_skills')
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE,related_name='blueprint_skills')
    question_count = models.PositiveIntegerField(default=3)
    priority = models.PositiveIntegerField(default=1)
    difficulty_distribution = models.JSONField(default=dict,blank=True)

    def __str__(self):
        return f'{self.blueprint} - {self.skill.name}'


class Question(models.Model):

    QUESTION_TYPE_CHOICES = [
        ('MCQ', 'Multiple Choice'),
        ('OPEN_ENDED', 'Open Ended'),
        ('CODE', 'Coding'),
    ]

    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    ]

    SOURCE_CHOICES = [
        ('AI', 'AI Generated'),
        ('ADMIN', 'Admin Created'),
        ('IMPORTED', 'Imported'),
    ]

    assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE,related_name='questions')
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE,related_name='assessment_questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20,choices=QUESTION_TYPE_CHOICES,default='MCQ')
    difficulty = models.CharField(max_length=10,choices=DIFFICULTY_CHOICES,default='MEDIUM')
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)
    source = models.CharField(max_length=20,choices=SOURCE_CHOICES,default='AI')
    ai_generated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:80]


class QuestionOption(models.Model):

    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class AssessmentAttempt(models.Model):

    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ABANDONED', 'Abandoned'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE,related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='IN_PROGRESS')
    total_score = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.assessment.title}'


class AssessmentAnswer(models.Model):

    attempt = models.ForeignKey(AssessmentAttempt,on_delete=models.CASCADE,related_name='answers')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='assessment_answers')
    selected_option = models.ForeignKey(QuestionOption,on_delete=models.SET_NULL,null=True,blank=True,related_name='selected_answers')
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True,blank=True)
    marks_awarded = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.attempt.user.username} - Question {self.question.id}'