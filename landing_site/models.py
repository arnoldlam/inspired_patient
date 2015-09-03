from django.db import models

# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=4000)
	date_created = models.DateTimeField('date created', auto_now_add=True)
	author_name = models.CharField(max_length = 100)