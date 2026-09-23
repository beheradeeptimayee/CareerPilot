from django.contrib import admin

# Register your models here.
from accounts.models import EmailVerification,StudentProfile

admin.site.register(EmailVerification)

admin.site.register(StudentProfile)
