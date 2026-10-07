from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from careers.models import Career, Skill


class LearningRoadmap(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVED', 'Archived'),
    ]

    user = models.ForeignKey( User,on_delete=models.CASCADE,related_name='learning_roadmaps')

    career = models.ForeignKey(Career,on_delete=models.CASCADE,related_name='learning_roadmaps')

    title = models.CharField(max_length=200)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='ACTIVE')

    overall_progress = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    estimated_duration_weeks = models.PositiveIntegerField(default=8)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'career'],
                name='unique_user_career_roadmap'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.career.name}'


class RoadmapSkill(models.Model):

    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    roadmap = models.ForeignKey(LearningRoadmap,on_delete=models.CASCADE,related_name='roadmap_skills')

    skill = models.ForeignKey(Skill,on_delete=models.CASCADE,related_name='roadmap_skills')

    priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='MEDIUM')

    current_score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    target_score = models.DecimalField(max_digits=5,decimal_places=2,default=70.00)

    gap_score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='NOT_STARTED')

    progress = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    order = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['roadmap', 'skill'],
                name='unique_roadmap_skill'
            )
        ]
        ordering = ['order']

    def __str__(self):
        return f'{self.roadmap} - {self.skill.name}'


class LearningModule(models.Model):

    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    roadmap_skill = models.ForeignKey(
        RoadmapSkill,
        on_delete=models.CASCADE,
        related_name='learning_modules'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=1)

    estimated_minutes = models.PositiveIntegerField(default=30)

    difficulty = models.CharField(max_length=20,choices=DIFFICULTY_CHOICES,default='BEGINNER')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['roadmap_skill', 'order'],
                name='unique_module_order_per_skill'
            )
        ]

        ordering = ['order']

    def __str__(self):
        return self.title


class UserModuleProgress(models.Model):

    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='module_progress')

    module = models.ForeignKey(LearningModule,on_delete=models.CASCADE,related_name='user_progress')

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='NOT_STARTED')

    progress = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)

    started_at = models.DateTimeField(null=True,blank=True)

    completed_at = models.DateTimeField(null=True,blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'module'],
                name='unique_user_module_progress'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.module.title}'