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
	url(r'^collaboration/search$', views.SearchUserResultsView, name='search_results'),
	url(r'^collaboration/profile/(?P<user_id>[0-9]+)$', views.PublicProfileView, name='public_profile'),
	url(r'^collaboration/add_associate/(?P<user_id>[0-9]+)$', views.AddAssociate, name='add_associate'),
	url(r'^clinics/$', views.ClinicView, name='clinics'),
	url(r'^clinics/(?P<clinic_id>[0-9]+)$', views.ClinicDetailView, name='clinic_detail'),
	url(r'^notes/$', views.NotesView, name='notes'),
	url(r'^notes/search$', views.HealthToolsSearchResultsView, name='health_tools_search_results'),
	url(r'^notes/(?P<note_id>[0-9]+)/$', views.NoteDetail, name='note_detail'),
	url(r'^notes/(?P<note_id>[0-9]+)/add_reply$', views.AddNoteReplyView, name='add_note_reply'),
	url(r'^notes/add/$', views.NotesSelectView, name='notes_select'),
	url(r'^notes/add/note/$', views.AddNoteView, name='add_note'),
	url(r'^notes/add/general_note$', views.AddGeneralNoteView, name='add_general_note'),
	url(r'^notes/add/instruction_note$', views.AddInstructionNoteView, name='add_instruction_note'),
	url(r'^notes/add/communication_note$', views.AddCommunicationNoteView, name='add_communication_note'),
	url(r'^notes/(?P<note_id>[0-9]+)/share$', views.ShareNote, name='share_note'),
	url(r'^notes/add_notebook/$', views.AddNotebookView, name='add_notebook'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/$', views.NotebookDetail, name='notebook_detail'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/add_notes', views.AddNotesToNotebookView, name='add_notes_to_notebook'),
	url(r'^notes/notebook/(?P<notebook_id>[0-9]+)/share', views.ShareNotebookView, name='share_notebook'),
	url(r'^notifications/$', views.NotificationsView, name='notifications'),
	url(r'^notifications/mark_as_read$', views.MarkNotificationAsRead, name='mark_notification_as_read'),
]