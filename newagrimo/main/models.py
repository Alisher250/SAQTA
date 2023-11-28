from django.db import models
from django.contrib.auth.models import User

class Hobby(models.Model):
    name = models.CharField('name of hobby', max_length=200)

    def __str__(self):
        return self.name

class Stories(models.Model):
    title = models.CharField('title of stories', max_length=200)
    content = models.TextField('text of stories')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    likes = models.IntegerField('likes of stories')
    photo = models.ImageField(upload_to='images_stories/', default=None)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.CharField('text of comments', max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stories = models.ForeignKey(Stories, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
