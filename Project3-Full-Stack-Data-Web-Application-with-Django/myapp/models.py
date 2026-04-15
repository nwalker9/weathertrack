from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length= 200)
    is_done = models.BooleanField(default=False)
    priority = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ({'done' if self.is_done else 'pending'})"