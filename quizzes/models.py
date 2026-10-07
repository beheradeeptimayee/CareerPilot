from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from roadmaps.models import LearningModule


class Quiz(models.Model):

    module = models.OneToOneField(LearningModule,on_delete=models.CASCADE,related_name='quiz')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    passing_score = models.DecimalField(max_digits=5,decimal_places=2,default=60.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):

    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=1)
    marks = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text[:80]


class QuizOption(models.Model):

    question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE,related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


class QuizAttempt(models.Model):

    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='attempts')
    score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='IN_PROGRESS')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title}'


class QuizAnswer(models.Model):

    attempt = models.ForeignKey(QuizAttempt,on_delete=models.CASCADE,related_name='answers' )
    question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE,related_name='answers')
    selected_option = models.ForeignKey(QuizOption,on_delete=models.CASCADE,related_name='selected_answers')
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.PositiveIntegerField(default=0)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['attempt', 'question'],
                name='unique_quiz_answer'
            )
        ]

    def __str__(self):
        return f'{self.attempt} - Question {self.question.order}'