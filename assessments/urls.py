from django.urls import path

from assessments import views


urlpatterns = [
    path('<slug:career_slug>/', views.assessment_intro,name='assessment_intro'),
    path('<slug:career_slug>/start/',views.start_assessment,name='start_assessment'),
    path('<slug:career_slug>/skill-gap/',views.skill_gap_analysis,name='skill_gap_analysis'),
    path('attempt/<int:attempt_id>/question/',views.assessment_question,name='assessment_question'),
    path('attempt/<int:attempt_id>/complete/',views.assessment_complete,name='assessment_complete'),
]