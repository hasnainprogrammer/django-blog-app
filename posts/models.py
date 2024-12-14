from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=200)
    body = models.TextField()
    publish_date = models.DateTimeField(blank=True, default=datetime.now())
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True)
    comment_date = models.DateTimeField(blank=True, default=datetime.now())

    def __str__(self):
        return self.comment_text
