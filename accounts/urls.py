from django.urls import path
from accounts import views


urlpatterns = [
path('register/', views.register, name='register'),
path('verify/<uuid:token>/',views.verify_email,name='verify_email'),
]