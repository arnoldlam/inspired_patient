from django import forms
from django.forms import ModelForm, MultipleChoiceField, ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from dashboard.models import UserProfile, DischargeNote, Notebook
from django.contrib.auth.models import User, Group
from dashboard.models import UserProfile

class AddNoteForm(forms.Form):
	def __init__(self, user_id, *args, **kwargs):
		super(AddNoteForm, self).__init__(*args, **kwargs)

		self.user_id = user_id
		current_user = User.objects.get(pk=self.user_id)
		associates = current_user.user_profile.associates.all()

		list_of_names = []
		for associate in associates:
			name = associate.full_name()
			list_of_names.append(name)
		self.user_choices = zip(associates, list_of_names)

		self.fields['choices_for_editors'] = forms.MultipleChoiceField(label='Editors', choices=self.user_choices, required=False)
		self.fields['choices_for_viewers'] = forms.MultipleChoiceField(label='Viewers', choices=self.user_choices, required=False)

	subject = forms.CharField(label='Subject', max_length=150)
	note_content = forms.CharField(label='Note', max_length=250, widget=forms.Textarea)
	attachment = forms.FileField(required=False)
	url = forms.URLField(label='URL', required=False)
	follow_up = forms.CharField(label='Follow-Up', required=False, max_length=250)

class AddInstructionNoteForm(AddNoteForm):
	instructions = forms.CharField(label='Instructions', max_length=400)

class AddCommunicationNoteForm(AddNoteForm):
	PRIORITY_CHOICES = (
		('read', 'Read'),
		('respond', 'Respond'),
		('urgent', 'Urgent'),
	)	
	attention = forms.CharField(max_length=250)
	importance = forms.ChoiceField(choices=PRIORITY_CHOICES)

class AddDischargeNoteForm(ModelForm):
	class Meta:
		model = DischargeNote
		fields = ['subject', 'note_content', 'procedure', 'doctor', 'weight', 'medication_dose', 
		'next_dose', 'selfcare_instructions', 'emergency_instructions']
		
class SearchForUserForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=60, required = False)

class EditProfileForm(forms.Form):
	ROLE_CHOICES = (
		('patient', 'Patient'),
		('caregiver', 'Caregiver'),
		('parent', 'Parent'),
		('professional', 'Professional'),
	)
	
	ADDRESS_CITY_CHOICES = (
		('CA', 'Canada'),
		('US', 'United States'),
		('UK', 'United Kingdom'),
	)

	profile_picture = forms.ImageField()
	title = forms.CharField(label='Title', max_length=15)	
	first_name = forms.CharField(label='First Name', max_length=20)
	last_name = forms.CharField(label='Last Name', max_length=20)
	role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES)

	address_unit = forms.CharField(label='Unit', max_length=10)
	address_street = forms.CharField(label='Street', max_length=50)
	address_city = forms.CharField(label='City', max_length=30)
	address_province = forms.CharField(label='Province', max_length=30)
	address_country = forms.ChoiceField(label='Country', choices=ADDRESS_CITY_CHOICES)
	address_postal_code = forms.CharField(label='Postal Code', max_length=10)

	medical_history = forms.CharField(label='Medical History', max_length=4000)
	phone_number = forms.CharField(label='Phone Number', max_length=20)

class AddNotebookForm(ModelForm):
	class Meta:
		model = Notebook
		fields = ['name', 'description']

# class AddSelfCareNoteForm(AddNoteForm):	
# 	selfcare_desc = forms.CharField(max_length=1000)
# 	frequency = forms.CharField(max_length=150)
# 	adverse_event_procedure = forms.CharField(max_length=250)
# 	procedure = forms.CharField(max_length=4000)
# 	time = forms.CharField(max_length=250)
# 	outcome = forms.CharField(max_length=250)	
# 	

# class AddMedicalInformationNoteForm(AddNoteForm):
# 	medication_name = forms.CharField(max_length=100)
# 	medication_dose = forms.CharField(max_length=100)
# 	medication_duration = forms.IntegerField()	
# 	

# class EditProfileForm(ModelForm):
# 	class Meta:
# 		model = UserProfile
# 		fields = ['profile_picture', 'title', 
# 		'role', 'address_street', 'address_city', 'address_country', 'address_province',
# 		'address_country', 'address_postal_code', 'medical_history', 'phone_number']
# 		first_name = forms.CharField(label='First Name', max_length=20)
# 		last_name = forms.CharField(label='Last Name', max_length=20)