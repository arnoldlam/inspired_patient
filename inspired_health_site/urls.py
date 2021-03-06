"""apps4kids URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from dashboard import views as dashboard_views
from landing_site import views as landing_site_views

urlpatterns = [
    url(r'^$', landing_site_views.IndexView, name='index'),
    url(r'^about_us/$', landing_site_views.AboutUsView, name='about_us'),
    url(r'^solutions/$', landing_site_views.SolutionsView, name='solutions'),
    url(r'^plans/$', landing_site_views.PlansView, name='plans'),
    url(r'^terms_of_use/$', landing_site_views.TermsOfUseView, name='terms_of_use'),
    url(r'^privacy_policy/$', landing_site_views.PrivacyPolicyView, name='privacy_policy'),
    url(r'^faq/$', landing_site_views.FAQView, name='faq'),
    url(r'^contact_us/$', landing_site_views.ContactUsView, name='contact_us'),
    url(r'^blog/$', landing_site_views.BlogView, name='blog'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup$', dashboard_views.CreateNewUserView, name='create_user'),
    url(r'^accounts/signup/continued$', dashboard_views.CreateNewUserExtendedView, name='create_user_extended'),
    url(r'^accounts/signup/professional$', dashboard_views.CreateNewProfessionalView, name='create_professional'),
]
