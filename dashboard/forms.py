from django import forms

class AddNoteForm(forms.Form):
	subject = forms.CharField(label='Subject', max_length=150)
	note_content = forms.CharField(label='Note', max_length=250)
	attachment = forms.FileField(required=False)
	url = forms.CharField(label='URL Link', max_length=500)
	follow_up = forms.CharField(label='Follow-Up', max_length=250)

class AddInstructionNoteForm(AddNoteForm):
	instructions = forms.CharField(label='Instructions', max_length=400)

class SearchForUserForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=60, required = False)

class EditProfileForm(forms.Form):
	title = forms.CharField(label='Title', max_length=15)	
	first_name = forms.CharField(label='First Name', max_length=20)
	last_name = forms.CharField(label='Last Name', max_length=20)

	address_unit = forms.CharField(label='Unit', max_length=10)
	address_street = forms.CharField(label='Street', max_length=50)
	address_city = forms.CharField(label='City', max_length=30)
	address_province = forms.CharField(label='Province', max_length=30)
	address_country = forms.CharField(label='Country', max_length=30)
	address_postal_code = forms.CharField(label='Postal Code', max_length=10)

	medical_history = forms.CharField(label='Medical History', max_length=4000)
	phone_number = forms.CharField(label='Phone Number', max_length=20)
	role = forms.CharField(label='Role', max_length=15)
	profile_picture = forms.ImageField()

class AddNotebookForm(forms.Form):
	name = forms.CharField(label='Notebook name', max_length=20)
	description = forms.CharField(label='Description', max_length=4000)


# class AddCommunicationNoteForm(AddNoteForm):	
# 	attention = forms.CharField(max_length=250)
# 	importance = forms.CharField(max_length=250)
# 	instructions = forms.CharField(max_length=4000)	
# 	# attachments needs to be added

# class AddDischargeNoteForm(AddNoteForm):	
# 	procedure = forms.CharField(max_length=250)
# 	doctor = forms.CharField(max_length=250)
# 	weight = forms.IntegerField(default=0)
# 	medication_name = forms.CharField(max_length=100)
# 	medication_dose = forms.CharField(max_length=100)
# 	next_dose = forms.CharField(max_length=100)
# 	selfcare_instructions = forms.CharField(max_length=4000)
# 	emergency_instructions = forms.CharField(max_length=4000)
# 	# attachments needs to be added

# class AddSelfCareNoteForm(AddNoteForm):	
# 	selfcare_desc = forms.CharField(max_length=1000)
# 	frequency = forms.CharField(max_length=150)
# 	adverse_event_procedure = forms.CharField(max_length=250)
# 	procedure = forms.CharField(max_length=4000)
# 	time = forms.CharField(max_length=250)
# 	outcome = forms.CharField(max_length=250)	
# 	# attachments needs to be added

# class AddMedicalInformationNoteForm(AddNoteForm):
# 	medication_name = forms.CharField(max_length=100)
# 	medication_dose = forms.CharField(max_length=100)
# 	medication_duration = forms.IntegerField()	
# 	# attachments needs to be added