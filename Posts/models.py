from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.CharField(max_length=250, null=False, blank=False)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title