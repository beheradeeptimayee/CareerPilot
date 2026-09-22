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

     