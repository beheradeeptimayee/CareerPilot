from django.contrib import admin

# Register your models here.
from roadmaps.models import LearningRoadmap,RoadmapSkill,LearningModule,UserModuleProgress

admin.site.register(LearningRoadmap)
admin.site.register(RoadmapSkill)
admin.site.register(LearningModule)
admin.site.register(UserModuleProgress)