"""
Filename: views.py
Created on: June 13th, 2015
Author: Arnold Lam
Description: Provides the models for the landing pages of Inspired Patient
"""

from django.db import models

# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_created = models.DateTimeField('date created', auto_now_add=True)
	author_name = models.CharField(max_length = 100)
	image = models.ImageField(upload_to='blog_pictures', blank=True)
	url = models.URLField(blank=True)

	def __unicode__(self):
		return self.title