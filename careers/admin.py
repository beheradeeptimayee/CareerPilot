from django.contrib import admin

# Register your models here.
from careers.models import Category,Skill,Career

admin.site.register(Category)

admin.site.register(Skill)

admin.site.register(Career)
