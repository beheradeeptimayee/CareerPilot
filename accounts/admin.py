from django.contrib import admin

# Register your models here.
from accounts.models import EmailVerification

admin.site.register(EmailVerification)