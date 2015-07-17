from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.

from .models import UserProfile, Clinic, Note, CommunicationNote, DischargeNote, InstructionNote, MedicalInformationNote, SelfCareNote, Notebook, Attachment

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'User Profile'
	fieldsets = (
		(None, {'fields': ('profile_picture', 'role', 'title', 'associates', 'phone_number', 
			'medical_history',)}),
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

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Clinic)
admin.site.register(Note)
admin.site.register(CommunicationNote)
admin.site.register(DischargeNote)
admin.site.register(InstructionNote)
admin.site.register(MedicalInformationNote)
admin.site.register(SelfCareNote)
admin.site.register(Notebook)
admin.site.register(Attachment)