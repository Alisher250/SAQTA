from django.contrib import admin
from .models import Stories, Hobby, Comment

# Register your models here.
admin.site.register(Stories)
admin.site.register(Hobby)
admin.site.register(Comment)