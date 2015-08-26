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
import urllib

class Address(models.Model):
	ADDRESS_COUNTRY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)

	street = models.CharField('Street', max_length=50)
	unit = models.CharField('Unit', max_length=10)
	city = models.CharField('City', max_length=30)
	province = models.CharField('Province / State', max_length=30)
	country = models.CharField('Country', max_length=30, choices = ADDRESS_COUNTRY_CHOICES, 
		default='CA')
	postal_code = models.CharField('Postal Code', max_length=10) 

	def __unicode__(self):
		return self.unit + " " + self.street + ", " + self.city + ", " + self.province

	def mapQuery(self):
		return self.unit + "+" + self.street + "+" + self.city

class UserProfile(models.Model):
	ADDRESS_CITY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
		('AU', 'Australia'),
	)
	ROLE_CHOICES = (
		('patient', 'Patient'),
		('caregiver', 'Caregiver'),
		('parent', 'Parent'),
		('professional', 'Professional'),
		('individual', 'Individual'),
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

	office_address_street = models.CharField('Office Street', max_length=50, blank=True)
	office_address_unit = models.CharField('Office Unit', max_length=10, blank=True)
	office_address_city = models.CharField('Office City', max_length=30, blank=True)
	office_address_province = models.CharField('Office Province / State', max_length=30, blank=True)
	office_address_country = models.CharField('Office Country', max_length=30, choices = ADDRESS_CITY_CHOICES, 
		default='CA', blank=True)
	office_address_postal_code = models.CharField('Office Postal Code', max_length=10, blank=True)

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

	def unreadNotificationCount(self):
		user = self.user
		count = 0
		for notification in user.notifications_received.all():
			if notification.view_status == 'unread':
				count += 1
		return count

class Clinic(models.Model):
	users = models.ManyToManyField(User, related_name='clinics')
	name = models.CharField(max_length=100)
	address = models.OneToOneField(Address, related_name="clinic")
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name
	
class Note(models.Model):
	NOTE_TYPE_CHOICES = (
		('general_note', 'General note'),
		('instruction_note', 'Instruction note'),
		('communication_note', 'Communication note'),
		('procedure_note', 'Procedure note'),
		('self_care_note', 'Self care note'),
		('resource_note', 'Resource note'),
		('appointment_note', 'Appointment note'), 
		('contact_note', 'Contact note'), 
		('medication_note', 'Medication note'),
	)
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

	# Optional date and time for some note types
	date_and_time = models.DateTimeField('Date and Time', blank=True, null=True)

	# Get font name for different note types
	def getFontAwesomeIconName(self):
		if self.note_type == 'general_note':
			return 'fa-sticky-note' 
		if self.note_type == 'instruction_note':
			return 'fa-list-ol'
		if self.note_type == 'communication_note':
			return 'fa-comments' 
		if self.note_type == 'procedure_note':
			return 'fa-stethoscope'
		if self.note_type == 'self_care_note':
			return 'fa-home' 
		if self.note_type == 'resource_note':
			return 'fa-file-text'
		if self.note_type == 'appointment_note':
			return 'fa-user-md'
		if self.note_type == 'contact_note':
			return 'fa-user' 
		if self.note_type == 'medication_note':
			return 'fa-medkit' 

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

class InstructionNote(Note):	
	instructions = models.CharField(max_length=4000)

class CommunicationNote(Note):	
	IMPORTANCE_CHOICES = (
		('read', 'Read'),
		('respond', 'Respond'),
		('urgent', 'Urgent'),
	)
	importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='read')
	doctor = models.ForeignKey(User, related_name='communication_notes_doctor', null=True, blank=True)
	clinic = models.ForeignKey(Clinic, related_name='communication_notes', null=True, blank=True)
	recipient_team_member = models.ForeignKey(User, related_name='communication_notes_team_member', null=True)

class ProcedureNote(Note):	
	procedure = models.TextField()
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	self_care_instructions = models.TextField()
	emergency_instructions = models.TextField()
	pre_procedure_instructions = models.TextField()
	follow_up_instructions = models.TextField()
	doctor = models.ForeignKey(User, related_name='procedure_notes', null=True)
	clinic = models.ForeignKey(Clinic, related_name='procedure_notes', null=True)

class SelfCareNote(Note):
	FREQUENCY_CHOICES = (
		('not_repeating', 'Not repeating'),
		('every_day', 'Every Day'),
		('every_week', 'Every Week'),
		('every_month', 'Every Month')
	)

	frequency = models.CharField(max_length=150, choices=FREQUENCY_CHOICES, default='not_repeating')
	description = models.TextField()
	emergency_procedure = models.TextField()
	procedure = models.TextField()
	outcome = models.CharField(max_length=250)

class ResourceNote(Note):
	doctor = models.ForeignKey(User, related_name='resource_notes', null=True)
	clinic = models.ForeignKey(Clinic, related_name='resource_notes', null=True)

class AppointmentNote(Note):
	FREQUENCY_CHOICES = (
		('not_repeating', 'Not repeating'),
		('every_day', 'Every Day'),
		('every_week', 'Every Week'),
		('every_month', 'Every Month')
	)

	frequency = models.CharField(max_length=150, choices=FREQUENCY_CHOICES, default='not_repeating')
	doctor = models.ForeignKey(User, related_name='appointments', null=True)
	clinic = models.ForeignKey(Clinic, related_name='appointments', null=True)
	reason_for_visit = models.CharField(max_length=200)

class ContactNote(Note):
	title = models.CharField(max_length=15)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	organization_name = models.CharField(max_length=100, blank=True)
	address = models.OneToOneField(Address, related_name='contact_notes', null=True)
	phone_number_work = models.CharField('Phone Number (Work)', max_length=20, blank=True)
	phone_number_home = models.CharField('Phone Number (Home)', max_length=20, blank=True)
	email = models.EmailField(blank=True)

	def full_name(self):
		return self.first_name + " " + self.last_name

class MedicationNote(Note):
	FREQUENCY_CHOICES = (
		('not_repeating', 'Not repeating'),
		('every_day', 'Every Day'),
		('every_week', 'Every Week'),
		('every_month', 'Every Month')
	)

	medication_frequency = models.CharField(max_length=150, choices=FREQUENCY_CHOICES, default='not_repeating')
	medication_name = models.CharField(max_length=100)
	medication_dosage = models.CharField(max_length=100)
	medication_duration = models.CharField(max_length=100)
	pharmacy_name = models.CharField(max_length=50)
	pharmacy_address = models.ForeignKey(Address, related_name='medication_notes')
	pharmacy_telephone = models.CharField(max_length=50)

class Notebook(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=4000, blank=True)
	viewers = models.ManyToManyField(User, related_name="notebooks_read_only", blank=True)
	editors = models.ManyToManyField(User, related_name="notebooks_read_write")
	notes = models.ManyToManyField(Note, related_name='notebooks', blank=True)
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


