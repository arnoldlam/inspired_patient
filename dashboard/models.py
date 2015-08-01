"""
Filename: models.py
Created on: June 13th, 2015
Author: Arnold Lam
Description: Provides the models for Inspired Health
"""

from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

class UserProfile(models.Model):
	ADDRESS_CITY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)
	ROLE_CHOICES = (
		('patient', 'Patient'),
		('caregiver', 'Caregiver'),
		('parent', 'Parent'),
		('professional', 'Professional'),
	)

	user = models.OneToOneField(User, related_name="user_profile")
	associates = models.ManyToManyField("self", blank=True)
	address_street = models.CharField('Street', max_length=50)
	address_unit = models.CharField('Unit', max_length=10)
	address_city = models.CharField('City', max_length=30)
	address_province = models.CharField('Province / State', max_length=30)
	address_country = models.CharField('Country', max_length=30, choices = ADDRESS_CITY_CHOICES, 
		default='CA')
	address_postal_code = models.CharField('Postal Code', max_length=10)
	phone_number = models.CharField(max_length=20)
	medical_history = models.CharField(max_length=4000, blank=True)
	role = models.CharField(max_length=15, choices = ROLE_CHOICES, default='patient') # ie. professional, patient
	title = models.CharField(max_length=15)
	profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

	# Optional fields for professionals
	qualification = models.CharField(max_length=250, blank=True)
	job_title = models.CharField('Job Title', max_length=100, blank=True)
	office_tel = models.CharField('Office Telephone', max_length=50, blank=True)
	office_email = models.EmailField('Office Email', blank=True)
	office_address = models.CharField('Office Address', max_length=250, blank=True)

	def __unicode__(self):
		return self.user.username

	def full_name(self):
		return self.user.first_name + " " + self.user.last_name

	# Takes in user object
	# Returns whether user is an associate of the user object
	def is_associate(self, other_user):
		if other_user.user_profile in self.associates.all():
			return 1
		else:
			return 0

class Clinic(models.Model):
	users = models.ManyToManyField(User, related_name='clinics')
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name
	
class Note(models.Model):
	NOTE_TYPE_CHOICES = (
		('general_note', 'General note'),
		('instruction_note', 'Instruction note'),
		('communication_note', 'Communication note'),
		('discharge_note', 'Discharge note'),
	)
	# For intermediate model
	# note_users = models.ManyToManyField(User, through='NoteUser')
	users = models.ManyToManyField(User, related_name='notes', blank=True)
	editors = models.ManyToManyField(User, related_name='notes_read_write', blank=True)
	viewers = models.ManyToManyField(User, related_name='notes_read_only', blank=True)
	author = models.ForeignKey(User, related_name='authored_notes', null=True)
	date_created = models.DateTimeField('date created', auto_now_add=True)
	date_accessed = models.DateTimeField('date accessed', auto_now_add=True)
	subject = models.CharField(max_length=150)
	follow_up = models.CharField(max_length=250, blank=True)
	note_content = models.TextField()
	note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES, default='general_note')
	url = models.URLField(max_length=200, blank=True)

	def __unicode__(self):
		return self.subject

	def noteAccessedNow(self):
		self.date_accessed = timezone.now()

	def getAuthor(self):
		return self.users.all()[0].first_name + " " + self.users.all()[0].last_name

	# Parameters: user_id
	# Returns: Boolean whether user can access note
	def ifUserCanAccessNote(self, user_id):
		if self.editors.filter(id=user_id).count > 0:
			return 1
		if self.viewers.filter(id=user_id).count > 0:
			return 1
		if self.author.filter(id=user_id).count > 0:
			return 1
		return 0

# Intermediate model describing relationship between Note and User
# class NoteUser(models.Model):
# 	PERMISSIONS_CHOICES = (
# 		('read_only', 'Read only'),
# 		('read_and_write', 'Read and write'),
# 	)

# 	note = models.ForeignKey(Note)
# 	user = models.ForeignKey(User)
# 	permissions = models.CharField('Note Permissions', max_length=30, choices=PERMISSIONS_CHOICES, default='read_only')
# 	date_accessed = models.DateTimeField('date accessed')

class InstructionNote(Note):	
	instructions = models.CharField(max_length=4000)

class CommunicationNote(Note):	
	IMPORTANCE_CHOICES = (
		('read', 'Read'),
		('respond', 'Respond'),
		('urgent', 'Urgent'),
	)
	attention = models.CharField(max_length=250)
	importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='read')

class ProcedureNote(Note):	
	procedure = models.CharField(max_length=250)
	doctor = models.CharField(max_length=250)
	weight = models.IntegerField()
	medication_name = models.CharField(max_length=100)
	medication_dose = models.CharField(max_length=100)
	next_dose = models.CharField(max_length=50)
	selfcare_instructions = models.TextField()
	emergency_instructions = models.TextField()
	

class SelfCareNote(Note):	
	selfcare_desc = models.CharField(max_length=1000)
	frequency = models.CharField(max_length=150)
	adverse_event_procedure = models.CharField(max_length=250)
	procedure = models.CharField(max_length=4000)
	time = models.CharField(max_length=250)
	outcome = models.CharField(max_length=250)	
	

class MedicalInformationNote(Note):
	medication_name = models.CharField(max_length=100)
	medication_dose = models.CharField(max_length=100)
	medication_duration = models.IntegerField()	
	

class Notebook(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=4000, blank=True)
	viewers = models.ManyToManyField(User, related_name="notebooks_read_only", blank=True)
	editors = models.ManyToManyField(User, related_name="notebooks_read_write")
	notes = models.ManyToManyField(Note, related_name='notes', blank=True)
	date_created = models.DateTimeField('date created', auto_now_add=True)
	date_modified = models.DateTimeField('date modified', auto_now_add=True)
	date_accessed = models.DateTimeField('date accessed', auto_now_add=True)

	def __unicode__(self):
		return self.name

class Attachment(models.Model):
	file_attachment = models.FileField(upload_to='attachments')
	note = models.ForeignKey(Note, related_name='attachments')
	name = file_attachment.name

	def __unicode__(self):
		return self.file_attachment.name

class NoteReply(models.Model):
	note = models.ForeignKey(Note, related_name='replies')
	title = models.CharField(max_length=100)
	content = models.TextField()
	author = models.ForeignKey(User, related_name='note_replies')
	date_created = models.DateTimeField('date created', auto_now_add=True)

	def __unicode__(self):
		return self.title


class Notification(models.Model):
	VIEW_STATUS_CHOICES = (
		('unread', 'Unread'),
		('read', 'Read'),
	)

	sender = models.ForeignKey(User, related_name='notifications_sent', blank=True, null=True)
	recipient = models.ForeignKey(User, related_name='notifications_received')
	view_status = models.CharField(max_length=15, choices=VIEW_STATUS_CHOICES, default='unread')
	message = models.CharField(max_length=400)
	action_url = models.URLField(blank=True)
	date_created = models.DateTimeField('date created', auto_now_add=True)
	date_read = models.DateTimeField('date accessed', null=True, blank=True)

	def __unicode__(self):
		return self.message


