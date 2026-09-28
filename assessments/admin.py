from django.contrib import admin

# Register your models here.
from assessments.models import *

admin.site.register(Assessment)
admin.site.register(AssessmentBlueprint)
admin.site.register(BlueprintSkill)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(AssessmentAttempt)
admin.site.register(AssessmentAnswer)
admin.site.register(AIEvaluation)
admin.site.register(SkillResult)
admin.site.register(ProficiencyLevel)