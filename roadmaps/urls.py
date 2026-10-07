from django.urls import path
from roadmaps import views


urlpatterns = [
    path('<slug:career_slug>/',views.roadmap_dashboard,name='roadmap_dashboard'),
    path('<slug:career_slug>/build/',views.build_roadmap,name='build_roadmap'),
    path('<slug:career_slug>/skill/<int:skill_id>/',views.skill_learning,name='skill_learning'),
    path('<slug:career_slug>/skill/<int:skill_id>/module/<int:module_id>/',views.module_learning,name='module_learning'),
]