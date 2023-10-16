from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class Task(models.Model):
    PRIORITY = (
        ('low', 'Low'),
        ('middle', 'Middle'),
        ('high', 'High')
    )
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title