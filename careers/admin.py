from django.contrib import admin

# Register your models here.
from careers.models import Category,Skill,Career,CareerSkill

admin.site.register(Category)

admin.site.register(Skill)

admin.site.register(Career)

admin.site.register(CareerSkill)