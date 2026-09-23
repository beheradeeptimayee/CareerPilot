from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import uuid

class EmailVerification(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

class StudentProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student_profile')
    # Personal Information
    phone = models.CharField(max_length=15,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=150,blank=True)
    
    # Education Information
    college = models.CharField(max_length=200,blank=True)
    degree = models.CharField(max_length=150,blank=True)
    year_of_passing = models.PositiveIntegerField(null=True,blank=True)
    cgpa = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)

    # Career Information
    career_goal = models.CharField(max_length=150,blank=True)
    areas_of_interest = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    preferred_job_role = models.CharField(max_length=150,blank=True)
    preferred_location = models.CharField(max_length=150,blank=True)
    willing_to_relocate = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
         