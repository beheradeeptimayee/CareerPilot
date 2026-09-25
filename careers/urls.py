from django.urls import path

from careers import views


urlpatterns = [
    path('', views.career_list, name='career_list'),
     path('<slug:slug>/',views.career_detail,name='career_detail'),
]