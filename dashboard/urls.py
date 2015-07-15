from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^$', views.Dashboard, name='dashboard'), # main landing page
	url(r'^profile/$', views.Profile, name='profile'),
	url(r'^profile/edit$', views.EditProfile, name='edit_profile'),
	url(r'^collaboration$', views.CollaborationView, name='collaboration'),
	url(r'^clinics/$', views.ClinicView, name='clinics'),
	url(r'^notes/$', views.NotesView, name='notes'),
	url(r'^notes/(?P<note_id>[0-9]+)/$', views.NoteDetail, name='note_detail'),
	url(r'^notes/add/$', views.NotesSelectView, name='notes_select'),
	url(r'^notes/add/note/$', views.AddNoteView, name='add_note'),
	url(r'^notes/(?P<note_id>[0-9]+)/share/$', views.ShareNote, name='share_note'),
	url(r'^notes/add_notebook/$', views.AddNotebookView, name='add_notebook'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/$', views.NotebookDetail, name='notebook_detail'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/add_notes', views.AddNotesToNotebookView, name='add_notes_to_notebook'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/share', views.ShareNotebookView, name='share_notebook'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)