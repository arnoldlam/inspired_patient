from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

class UserProfile(models.Model):

	user = models.OneToOneField(User, related_name="user_profile")
	associates = models.ManyToManyField("self", blank=True)
	address = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=20)
	medical_history = models.CharField(max_length=4000)
	role = models.CharField(max_length=15) # ie. professional, patient
	title = models.CharField(max_length=15)
	profile_picture = models.ImageField(upload_to='dashboard/static/dashboard/media/profile_pictures')

	def __str__(self):
		return self.user.username

	def full_name(self):
		return self.user.first_name + " " + self.user.last_name

class Clinic(models.Model):
	users = models.ManyToManyField(User, related_name='clinics')
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	phone_number = models.IntegerField()
	
class Note(models.Model):
	users = models.ManyToManyField(User, related_name='notes')
	author = models.ForeignKey(User, related_name='authored_notes', blank=True, null=True)
	date_created = models.DateTimeField('date created', auto_now_add=True)
	date_accessed = models.DateTimeField('date accessed')
	subject = models.CharField(max_length=150)
	follow_up = models.CharField(max_length=250)
	note_content = models.CharField(max_length=250)
	note_type = models.CharField(max_length=20)
	
	def __str__(self):
		return self.subject

	def noteAccessedNow(self):
		self.date_accessed = timezone.now()

	def getAuthor(self):
		return self.users.all()[0].first_name + " " + self.users.all()[0].last_name

	# Parameters: user_id
	# Returns: Boolean whether user can access note
	def ifUserCanAccessNote(self, user_id):
		for user in self.users.all():
			if user.id == user_id:
				return 1
		return 0


class InstructionNote(Note):	
	instructions = models.CharField(max_length=4000)
	# attachments needs to be added	


class CommunicationNote(Note):	
	attention = models.CharField(max_length=250)
	importance = models.CharField(max_length=250)
	instructions = models.CharField(max_length=4000)	
	# attachments needs to be added

class DischargeNote(Note):	
	procedure = models.CharField(max_length=250)
	doctor = models.CharField(max_length=250)
	weight = models.IntegerField(default=0)
	medication_name = models.CharField(max_length=100)
	medication_dose = models.CharField(max_length=100)
	next_dose = models.CharField(max_length=100)
	selfcare_instructions = models.CharField(max_length=4000)
	emergency_instructions = models.CharField(max_length=4000)
	# attachments needs to be added

class SelfCareNote(Note):	
	selfcare_desc = models.CharField(max_length=1000)
	frequency = models.CharField(max_length=150)
	adverse_event_procedure = models.CharField(max_length=250)
	procedure = models.CharField(max_length=4000)
	time = models.CharField(max_length=250)
	outcome = models.CharField(max_length=250)	
	# attachments needs to be added

class MedicalInformationNote(Note):
	medication_name = models.CharField(max_length=100)
	medication_dose = models.CharField(max_length=100)
	medication_duration = models.IntegerField()	
	# attachments needs to be added

class Notebook(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=4000, blank=True)
	viewers = models.ManyToManyField(User, related_name="notebooks_read_only", blank=True)
	editors = models.ManyToManyField(User, related_name="notebooks_read_write")
	notes = models.ManyToManyField(Note, related_name='notes', blank=True)

	def __str__(self):
		return self.name

class Attachment(models.Model):
	file_attachment = models.FileField(upload_to='dashboard/static/dashboard/attachments')
	note = models.ForeignKey(Note, related_name='attachments')
	name = file_attachment.name

	def __str__(self):
		return self.file_attachment.name
