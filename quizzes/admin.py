from django.contrib import admin

# Register your models here.
from quizzes.models import *

admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizOption)
admin.site.register(QuizAttempt)
admin.site.register(QuizAnswer)