from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.

from .models import UserProfile, Clinic, Note, CommunicationNote, ProcedureNote, InstructionNote, ResourceNote, SelfCareNote, Notebook, Attachment, NoteReply, Notification

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'User Profile'
	fieldsets = (
		(None, {'fields': ('profile_picture', 'role', 'title', 'associates', 'phone_number', 
			'medical_history', )}),
		('Address', {'fields':['address_unit', 'address_street', 'address_city', 'address_province', 'address_country', 'address_postal_code'],
		 'classes':['show']}),
	)

class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )
	fieldsets = (
		('Basic Information', {'fields': (('username', 'password'), ('first_name', 'last_name'), 'email',)}),
		('Date Information' , {'fields': ('last_login', 'date_joined',)}),
		('User Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',),})
	)

class RepliesInline(admin.TabularInline):
	model = NoteReply
	extra = 1

class AttachmentInline(admin.TabularInline):
	model = Attachment
	extra = 1

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
	list_display = ('subject', 'author', 'date_created', 'date_accessed', 'note_type', )
	fieldsets = (
		(None, {'fields': ('subject', 'note_type', 'note_content', 'url', 'follow_up',)}),
		('Users', {'fields':['author', 'editors', 'users', 'viewers'],'classes':['show']}),
	)
	inlines=[RepliesInline, AttachmentInline]
	list_filter = ['date_created']
	search_fields = ['subject', 'note_content']

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'email', 'phone_number', )
	fieldsets = (
		(None, {'fields': ('name', 'address', 'email', 'phone_number', 'users',)}),
	)

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'date_created', 'date_modified', 'date_accessed')
	fieldsets = (
		(None, {'fields': ('name', 'description', 'notes')}),
		('Users', {'fields':['editors',],'classes':['show']}),
	)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
# admin.site.register(CommunicationNote)
# admin.site.register(ProcedureNote)
admin.site.register(InstructionNote)
# admin.site.register(MedicalInformationNote)
# admin.site.register(SelfCareNote)
# admin.site.register(Notebook)
admin.site.register(Attachment)
admin.site.register(NoteReply)
admin.site.register(Notification)
admin.site.register(UserProfile)
