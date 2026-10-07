from django.urls import path

from quizzes import views


urlpatterns = [

    path('start/<int:quiz_id>/',views.quiz_start,name='quiz_start'),
    path('attempt/<int:attempt_id>/',views.quiz_question,name='quiz_question'),
    path('attempt/<int:attempt_id>/complete/',views.quiz_complete,name='quiz_complete'),

]