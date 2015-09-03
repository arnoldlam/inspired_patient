from django.shortcuts import render
from landing_site.models import Blog

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
	blogs = Blog.objects.all()

	return render(request, 'landing_site/blogs.html', {
		'blogs':blogs,
	})