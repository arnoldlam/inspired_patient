from django.db import models

# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_created = models.DateTimeField('date created', auto_now_add=True)
	author_name = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='blog_pictures', blank=True)
	url = models.URLField(blan=True)

	def __unicode__(self):
		return self.title