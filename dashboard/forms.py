"""
Filename: forms.py
Created on: June 13th, 2015
Author: Arnold Lam
Description: Provides the forms for Inspired Patient
"""

from django import forms
from django.forms import ModelForm, MultipleChoiceField, ValidationError, ModelChoiceField
from django.forms.widgets import CheckboxSelectMultiple, Select, DateTimeInput
from dashboard.models import UserProfile, ProcedureNote, Notebook, NoteReply
from django.contrib.auth.models import User, Group
from dashboard.models import UserProfile
from django.db.models import Q
from django.utils import timezone
import datetime
from django.utils.translation import gettext as _

"""

Note related forms

"""

class UserPermissionsForm(forms.Form):
	def __init__(self, user_id, *args, **kwargs):
		super(UserPermissionsForm, self).__init__(*args, **kwargs)

		self.user_id = user_id
		current_user = User.objects.get(pk=self.user_id)
		associates = current_user.user_profile.associates.all()

		list_of_names = []
		for associate in associates:
			name = associate.full_name()
			list_of_names.append(name)
		self.user_choices = zip(associates, list_of_names)

		self.fields['choices_for_editors'] = forms.MultipleChoiceField(label='Editors', choices=self.user_choices, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control'}))
		self.fields['choices_for_viewers'] = forms.MultipleChoiceField(label='Viewers', choices=self.user_choices, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control'}))


class AddNoteForm(forms.Form):
	def __init__(self, user_id, *args, **kwargs):
		super(AddNoteForm, self).__init__(*args, **kwargs)

		self.user_id = user_id
		current_user = User.objects.get(pk=self.user_id)
		associates = current_user.user_profile.associates.all()
		notebooks = Notebook.objects.filter(Q(editors__id=user_id)).distinct()

		list_of_names = []
		for associate in associates:
			name = associate.full_name()
			list_of_names.append(name)
		self.user_choices = zip(associates, list_of_names)

		list_of_notebooks = []
		notebook_ids = []
		for notebook in notebooks:
			name = notebook.name
			list_of_notebooks.append(name)
			notebook_ids.append(notebook.id)
		self.notebook_choices = zip(notebook_ids, list_of_notebooks)

		self.fields['choices_for_editors'] = forms.MultipleChoiceField(label='Editors', choices=self.user_choices, required=False, 
			widget=forms.SelectMultiple(attrs={'class':'form-control'}))
		self.fields['choices_for_viewers'] = forms.MultipleChoiceField(label='Viewers', choices=self.user_choices, required=False, 
			widget=forms.SelectMultiple(attrs={'class':'form-control'}))
		self.fields['notebook_id'] = forms.MultipleChoiceField(choices=self.notebook_choices, required=False, 
			widget=forms.SelectMultiple(attrs={'class':'form-control'}))

	subject = forms.CharField(label='Subject', max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	note_content = forms.CharField(label='Note', max_length=4000, widget=forms.Textarea(attrs={'class':'form-control', 'rows':'20', 'required':'required'}))
	attachment = forms.FileField(required=False)
	url = forms.URLField(label='URL', required=False, widget=forms.URLInput(attrs={'class':'form-control','type':'url','placeholder':'eg. http://www.inspiredpatient.com'}))
	follow_up = forms.CharField(label='Follow-Up', required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control'}))

class AddInstructionNoteForm(AddNoteForm):
	instructions = forms.CharField(label='Instructions', max_length=400, widget=forms.Textarea(attrs={'class':'form-control','row':'10','required':'required'}))

class NotesThatRelateToDoctorAndClinic(AddNoteForm):
	def __init__(self, user_id, *args, **kwargs):
		super(NotesThatRelateToDoctorAndClinic, self).__init__(user_id, *args, **kwargs)
		user = User.objects.get(pk=self.user_id)
		doctors = user.user_profile.associates.filter(role__exact="professional")
		clinics = user.clinics.all()
		team_members = user.user_profile.associates.all()

		self.fields['choice_for_team_member'] = forms.ModelChoiceField(label='Team Member', queryset=team_members, 
			empty_label="Select a Team Member", required=False, widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['choice_for_doctor'] = forms.ModelChoiceField(label='Doctor', queryset=doctors, 
			empty_label="Select a Doctor", required=False, widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['choice_for_clinic'] = forms.ModelChoiceField(label='Clinic', queryset=clinics, 
			empty_label="Select a Clinic", required=False, widget=forms.Select(attrs={'class':'form-control'}))

class AddCommunicationNoteForm(NotesThatRelateToDoctorAndClinic):
	IMPORTANCE_CHOICES = (
		('read', 'Read'),
		('respond', 'Respond'),
	)	

	note_content = forms.CharField(label='Note', max_length=4000, widget=forms.Textarea(attrs={'class':'form-control', 'rows':'20', 'required':'required','placeholder':'Do not use this form for urgent or immediate communication. Expect delays in responses when using this form.'}))
	importance = forms.ChoiceField(choices=IMPORTANCE_CHOICES, widget=forms.Select(attrs={'class':'form-control','required':'required'}))

class AddProcedureNoteForm(NotesThatRelateToDoctorAndClinic):
	note_content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}), required=False)
	procedure = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class':'form-control','required':'required'}))
	weight = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0,widget=forms.TextInput(attrs={'class':'form-control','required':'required','type':'number'}))
	self_care_instructions = forms.CharField(label="Self Care Instructions", max_length=1000, 
		widget=forms.Textarea(attrs={'class':'form-control','required':'required'}))
	emergency_instructions = forms.CharField(label="Emergency Instructions", max_length=1000, 
		widget=forms.Textarea(attrs={'class':'form-control','required':'required'}))
	pre_procedure_instructions = forms.CharField(label="Pre-Procedure Instructions", max_length=1000, 
		widget=forms.Textarea(attrs={'class':'form-control','required':'required'}))
	follow_up_instructions = forms.CharField(label="Follow-Up Instructions", max_length=1000, 
		widget=forms.Textarea(attrs={'class':'form-control','required':'required'}))

class RepeatingNotesForm(AddNoteForm):
	def __init__(self, user_id, *args, **kwargs):
		super(RepeatingNotesForm, self).__init__(user_id, *args, **kwargs)
		self.day_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
			19,20,21,22,23,24,25,26,27,28,29,30,31]
		self.DAY_CHOICES = zip(self.day_list, self.day_list)

		self.MONTH_CHOICES = (
			('01', 'Jan'),
			('02', 'Feb'),
			('03', 'Mar'),
			('04', 'Apr'),
			('05', 'May'),
			('06', 'Jun'),
			('07', 'Jul'),
			('08', 'Aug'),
			('09', 'Sept'),
			('10', 'Oct'),
			('11', 'Nov'),
			('12', 'Dec'),
		)

		self.YEAR_CHOICES = (
			('2015','2015'),
			('2016','2016'),
			('2017','2017'),
		)

		self.HOUR_CHOICES = (
			('01', '01'),
			('02', '02'),
			('03', '03'),
			('04', '04'),
			('05', '05'),
			('06', '06'),
			('07', '07'),
			('08', '08'),
			('09', '09'),
			('10', '10'),
			('11', '11'),
			('12', '12'),
		)

		def createMinuteChoices():
			minute_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
			for minute in range(10,60):
				minute_list.append(minute)
			return zip(minute_list, minute_list)

		def get_current_hour():
			current_hour = int(datetime.datetime.now().strftime('%H'))
			if current_hour > 12:
				return current_hour - 12
			else:
				return current_hour

		self.MINUTE_CHOICES = createMinuteChoices()

		self.AM_PM_CHOICES = (
			('AM', 'AM'),
			('PM', 'PM'),
		)

		self.FREQUENCY_TYPE_CHOICES = (
			('hours', 'Hour(s)'),
			('days', 'Day(s)'),
			('weeks', 'Week(s)'),
		)

		self.current_month = datetime.datetime.now().strftime('%m')
		self.current_day = datetime.datetime.now().strftime('%d')
		self.current_year = datetime.datetime.now().strftime('%Y')

		self.current_hour = datetime.get_current_hour()
		self.current_minute = datetime.datetime.now().strftime('%M')
		self.current_am_pm = datetime.datetime.now().strftime('%p')

class AddSelfCareNoteForm(RepeatingNotesForm):
	def __init__(self, user_id, *args, **kwargs):
		super(AddSelfCareNoteForm, self).__init__(user_id, *args, **kwargs)

		self.fields['day'] = forms.ChoiceField(initial=self.current_day,choices=self.DAY_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['month'] = forms.ChoiceField(initial=self.current_month,choices=self.MONTH_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:35%;'}))
		self.fields['year'] = forms.ChoiceField(initial=self.current_year,choices=self.YEAR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['hour'] = forms.ChoiceField(initial=self.current_hour,choices=self.HOUR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['minute'] = forms.ChoiceField(initial=self.current_minute,choices=self.MINUTE_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['am_pm']= forms.ChoiceField(initial=self.current_am_pm,choices=self.AM_PM_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))

		self.fields['end_day'] = forms.ChoiceField(initial=self.current_day,choices=self.DAY_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['end_month'] = forms.ChoiceField(initial=self.current_month,choices=self.MONTH_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:35%;'}))
		self.fields['end_year'] = forms.ChoiceField(initial=self.current_year,choices=self.YEAR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['end_hour'] = forms.ChoiceField(initial=self.current_hour,choices=self.HOUR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['end_minute'] = forms.ChoiceField(initial=self.current_minute,choices=self.MINUTE_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['end_am_pm'] = forms.ChoiceField(initial=self.current_am_pm,choices=self.AM_PM_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))

		self.fields['frequency'] = forms.IntegerField(initial="0",widget=forms.NumberInput(attrs={'class':'form-control', 
			'required':'required','type':'number','style':'display:inline;width:10%;'}))
		self.fields['frequency_type'] = forms.ChoiceField(choices=self.FREQUENCY_TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:15%;'}))

	description = forms.CharField(label='Description', max_length=4000, 
		widget=forms.Textarea(attrs={'class':'form-control', 'required':'required'}))
	procedure = forms.CharField(label='Procedure', max_length=500, 
		widget=forms.Textarea(attrs={'class':'form-control', 'required':'required'}))
	emergency_procedure = forms.CharField(label='Emergency Procedure', max_length=500, 
		widget=forms.Textarea(attrs={'class':'form-control', 'required':'required'}))
	outcome = forms.CharField(label='Outcome', required=False, max_length=250,
		widget=forms.TextInput(attrs={'class':'form-control'}))
	note_content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}), 
		required=False)

class AddResourceNoteForm(NotesThatRelateToDoctorAndClinic):
	def __init__(self, user_id, *args, **kwargs):
		super(AddResourceNoteForm, self).__init__(user_id, *args, **kwargs)



class AddAppointmentNoteForm(NotesThatRelateToDoctorAndClinic, RepeatingNotesForm):
	def __init__(self, user_id, *args, **kwargs):
		super(AddAppointmentNoteForm, self).__init__(user_id, *args, **kwargs)

		self.fields['day'] = forms.ChoiceField(initial=self.current_day,choices=self.DAY_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['month'] = forms.ChoiceField(initial=self.current_month,choices=self.MONTH_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:35%;'}))
		self.fields['year'] = forms.ChoiceField(initial=self.current_year,choices=self.YEAR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['hour'] = forms.ChoiceField(initial=self.current_hour,choices=self.HOUR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['minute'] = forms.ChoiceField(initial=self.current_minute,choices=self.MINUTE_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['am_pm']= forms.ChoiceField(initial=self.current_am_pm,choices=self.AM_PM_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))

	note_content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}), required=False)	
	reason_for_visit = forms.CharField(label="Reason for Visit", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))

class AddContactNoteForm(AddNoteForm):
	ADDRESS_COUNTRY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)

	subject = forms.CharField(required=False)
	title = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	organization_name = forms.CharField(label='Organization name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	phone_number_work = forms.CharField(label='Work Phone', max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	phone_number_home = forms.CharField(label='Home Phone', max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=False)

	unit = forms.CharField(label='Unit', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	street = forms.CharField(label='Street', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	city = forms.CharField(label='City', max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	province = forms.CharField(label='Province', max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
	country = forms.ChoiceField(label='Country', choices=ADDRESS_COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'form-control'}),required=False)
	postal_code = forms.CharField(label='Postal Code', max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}),required=False)

class AddMedicationNoteForm(RepeatingNotesForm):
	ADDRESS_COUNTRY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)

	def __init__(self, user_id, *args, **kwargs):
		super(AddMedicationNoteForm, self).__init__(user_id, *args, **kwargs)

		self.fields['day'] = forms.ChoiceField(initial=self.current_day,choices=self.DAY_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['month'] = forms.ChoiceField(initial=self.current_month,choices=self.MONTH_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:35%;'}))
		self.fields['year'] = forms.ChoiceField(initial=self.current_year,choices=self.YEAR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['hour'] = forms.ChoiceField(initial=self.current_hour,choices=self.HOUR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['minute'] = forms.ChoiceField(initial=self.current_minute,choices=self.MINUTE_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['am_pm']= forms.ChoiceField(initial=self.current_am_pm,choices=self.AM_PM_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))

		self.fields['end_day'] = forms.ChoiceField(initial=self.current_day,choices=self.DAY_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['end_month'] = forms.ChoiceField(initial=self.current_month,choices=self.MONTH_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:35%;'}))
		self.fields['end_year'] = forms.ChoiceField(initial=self.current_year,choices=self.YEAR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['end_hour'] = forms.ChoiceField(initial=self.current_hour,choices=self.HOUR_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:30%;'}))
		self.fields['end_minute'] = forms.ChoiceField(initial=self.current_minute,choices=self.MINUTE_CHOICES,widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))
		self.fields['end_am_pm'] = forms.ChoiceField(initial=self.current_am_pm,choices=self.AM_PM_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:25%;'}))

		self.fields['frequency'] = forms.IntegerField(initial="0",widget=forms.NumberInput(attrs={'class':'form-control', 
			'required':'required','type':'number','style':'display:inline;width:10%;'}))
		self.fields['frequency_type'] = forms.ChoiceField(choices=self.FREQUENCY_TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control date_select', 
			'required':'required','style':'display:inline;width:15%;'}))

	note_content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5'}), required=False)	
	medication_name = forms.CharField(label='Medication Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	medication_dosage = forms.CharField(label='Medication Dosage', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	medication_duration = forms.CharField(label='Medication Duration', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	pharmacy_name = forms.CharField(label='Pharmacy Name', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	pharmacy_telephone = forms.CharField(label='Pharmacy Tel', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))

	unit = forms.CharField(label='Unit', max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	street = forms.CharField(label='Street', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	city = forms.CharField(label='City', max_length=30, initial="Vancouver", widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	province = forms.CharField(label='Province', max_length=30, initial="BC", widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	country = forms.ChoiceField(label='Country', choices=ADDRESS_COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'required':'required'}))
	postal_code = forms.CharField(label='Postal Code', max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))

class SearchForUserForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=60, required = False)

class AddNotebookForm(forms.Form):
	def __init__(self, user_id, *args, **kwargs):
		super(AddNotebookForm, self).__init__(*args, **kwargs)

		self.user_id = user_id
		current_user = User.objects.get(pk=self.user_id)
		associates = current_user.user_profile.associates.all()

		list_of_names = []
		for associate in associates:
			name = associate.full_name()
			list_of_names.append(name)
		self.user_choices = zip(associates, list_of_names)

		self.fields['name'] = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
		self.fields['description'] = forms.CharField(max_length=4000, required=False, widget=forms.TextInput(attrs={'class':'form-control',}))
		self.fields['choices_for_editors'] = forms.MultipleChoiceField(label='Editors', choices=self.user_choices, required=False,
			widget=forms.SelectMultiple(attrs={'class':'form-control',}))
		self.fields['choices_for_viewers'] = forms.MultipleChoiceField(label='Viewers', choices=self.user_choices, required=False,
			widget=forms.SelectMultiple(attrs={'class':'form-control',}))

class AddNoteReplyForm(forms.Form):
	content = forms.CharField(max_length=1000)

"""

User-related forms

"""

# Taken from Django Docs. Modified to include email instead of username
class UserCreationForm(forms.ModelForm):
	"""
	A form that creates a user, with no privileges, from the given username and
	password.
	"""
	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
		'email_in_use': _("The email you request is already in use."),
	}
	email = forms.EmailField(help_text=_("Please enter your real email address"), widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
	password1 = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label=_("Password confirmation"),
		widget=forms.PasswordInput(attrs={'class':'form-control'}),
		help_text=_("Enter the same password as above, for verification."))
	terms_of_use_check = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'required':'required'}))
	
	class Meta:
		model = User
		fields = ("username",)
		exclude = ("username",)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.username = self.cleaned_data["email"]
		user.email = self.cleaned_data["email"]
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserProfileCreationForm(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))
	last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'required':'required'}))


class UserProfileCreationExtendedForm(forms.Form):
	ROLE_CHOICES = (
		('individual', 'Individual'),
		('professional', 'Professional'),
	)

	TITLE_CHOICES = (
		('mr', 'Mr.'),
		('ms', 'Ms.'),
		('mrs', 'Mrs.'),
		('dr', 'Dr.'),
		('nurse', 'Nurse'),
	)

	ADDRESS_COUNTRY_CHOICES = (
		('', 'Country'),
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)

	profile_picture = forms.ImageField(required=False)
	title = forms.ChoiceField(required=False,choices=TITLE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
	role = forms.ChoiceField(required=False,choices=ROLE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
	phone_number = forms.CharField(required=False,max_length=15, widget=forms.TextInput(attrs={'class':'form-control'}))
	medical_history = forms.CharField(required=False,max_length=1000, widget=forms.Textarea(attrs={'class':'form-control', 'rows':'10'}))
	unit = forms.CharField(required=False,max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(required=False,max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	city = forms.CharField(required=False,max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	province = forms.CharField(required=False,max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	country = forms.ChoiceField(required=False,choices=ADDRESS_COUNTRY_CHOICES,widget=forms.Select(attrs={'class':'form-control'}))
	postal_code = forms.CharField(required=False,max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))

class CreateProfessionalProfileForm(forms.Form):
	qualification = forms.CharField(label='Qualification', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	job_title = forms.CharField(label='Job Title', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	office_tel = forms.CharField(label='Office Tel', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	office_email = forms.EmailField(label='Office Email', max_length=60, widget=forms.TextInput(attrs={'class':'form-control'}))

	ADDRESS_COUNTRY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
		('AU', 'Australia')
	)

	unit = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
	street = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	city = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	province = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
	country = forms.ChoiceField(choices=ADDRESS_COUNTRY_CHOICES)
	postal_code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))

class EditProfileForm(forms.Form):
	def __init__(self, user_id, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

		self.user_id = user_id
		current_user = User.objects.get(pk=self.user_id)
		current_user_profile = current_user.user_profile

		ROLE_CHOICES = (
			('individual', 'Individual'),
			('professional', 'Professional'),
		)
		ADDRESS_CITY_CHOICES = (
			('CA', 'Canada'),
			('US', 'United States'),
			('UK', 'United Kingdom'),
			('AU', 'Australia'),
		)

		TITLE_CHOICES = (
			('mr', 'Mr.'),
			('ms', 'Ms.'),
			('mrs', 'Mrs.'),
			('dr', 'Dr.'),
			('nurse', 'Nurse'),
		)

		self.fields['title'] = forms.ChoiceField(label='Role', choices=TITLE_CHOICES, initial=current_user_profile.title,
			widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['first_name'] = forms.CharField(label='First Name', max_length=20, initial=current_user.first_name,
			widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
		self.fields['last_name'] = forms.CharField(label='Last Name', max_length=20, initial=current_user.last_name,
			widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
		self.fields['profile_picture'] = forms.ImageField(required=False)
		self.fields['role'] = forms.ChoiceField(label='Role', choices=ROLE_CHOICES, initial=current_user_profile.role,
			widget=forms.Select(attrs={'class':'form-control','required':'required'}))
		self.fields['medical_history'] = forms.CharField(required=False, max_length=4000, initial=current_user_profile.medical_history,
			widget=forms.Textarea(attrs={'class':'form-control','rows':'10'}))
		self.fields['phone_number'] = forms.CharField(required=False, max_length=20, initial=current_user_profile.phone_number,
			widget=forms.TextInput(attrs={'class':'form-control'}))

		self.fields['address_unit'] = forms.CharField(required=False, max_length=10, initial=current_user_profile.address_unit,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['address_street'] = forms.CharField(required=False, max_length=50, initial=current_user_profile.address_street,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['address_city'] = forms.CharField(required=False, max_length=30, initial=current_user_profile.address_city,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['address_province'] = forms.CharField(required=False, max_length=30, initial=current_user_profile.address_province,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['address_country'] = forms.ChoiceField(required=False, choices=ADDRESS_CITY_CHOICES, initial=current_user_profile.address_country,
			widget=forms.Select(attrs={'class':'form-control'}))
		self.fields['address_postal_code'] = forms.CharField(required=False, max_length=10, initial=current_user_profile.address_postal_code,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['job_title'] = forms.CharField(required=False,max_length=100, initial=current_user_profile.job_title,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['qualification'] = forms.CharField(required=False,max_length=100, initial=current_user_profile.qualification,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['office_tel'] = forms.CharField(required=False,max_length=20, initial=current_user_profile.office_tel,
			widget=forms.TextInput(attrs={'class':'form-control'}))
		self.fields['office_email'] = forms.CharField(required=False, max_length=100, initial=current_user_profile.office_email,
			widget=forms.TextInput(attrs={'class':'form-control'}))


