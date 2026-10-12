from django.urls import path

from progress import views


urlpatterns = [
    path('<slug:career_slug>/',views.progress_dashboard,name='progress_dashboard'),
]