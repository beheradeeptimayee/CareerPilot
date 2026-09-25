from django.db import models

# Create your models here.

# For Category
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    description=models.TextField(blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

# For Skill
class Skill(models.Model):
    name=models.CharField(max_length=100,unique=True)

    description=models.TextField(blank=True)

    is_active=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# For Career
class Career(models.Model):
    name=models.CharField(max_length=100,unique=True)

    slug=models.SlugField(unique=True)

    description=models.TextField()

    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='careers')

    skills=models.ManyToManyField(Skill,related_name='careers',blank=True)

    icon=models.CharField(max_length=10,blank=True)

    is_active=models.BooleanField(default=True)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
