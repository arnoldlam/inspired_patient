"""
Filename: views.py
Created on: June 13th, 2015
Author: Arnold Lam
Description: Provides the views for the landing pages for Inspired Patient
"""

from django.shortcuts import render
from landing_site.models import Blog
from dashboard.models import Privacy

# Create your views here.

def IndexView(request):
	return render(request, 'landing_site/index.html',)

def AboutUsView(request):
	return render(request, 'landing_site/about_us.html',)

def SolutionsView(request):
	return render(request, 'landing_site/solutions.html',)

def PlansView(request):
	return render(request, 'landing_site/plans.html',)

def FAQView(request):
	return render(request, 'landing_site/faq.html',)

def ContactUsView(request):
	return render(request, 'landing_site/contact_us.html',)

def BlogView(request):
	blogs = Blog.objects.all().order_by('-date_created')

	return render(request, 'landing_site/blogs.html', {
		'blogs':blogs,
	})

def TermsOfUseView(request):
	privacy = Privacy.objects.get(id=1)

	return render(request, 'landing_site/terms_of_use.html', {
		'privacy':privacy,
	})

def PrivacyPolicyView(request):
	privacy = Privacy.objects.get(id=1)

	return render(request, 'landing_site/privacy_policy.html', {
		'privacy':privacy,
	})