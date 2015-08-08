"""
Filename: views.py
Created on: June 13th, 2015
Author: Arnold Lam
Description: Provides the views for Inspired Health
"""

from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone
from django.db.models import Q
import datetime

from django.contrib.auth.models import User, Group
from dashboard.models import Clinic, UserProfile, Note, InstructionNote, Attachment, Notebook, CommunicationNote, ProcedureNote, NoteReply, Notification, SelfCareNote, ResourceNote, AppointmentNote, ContactNote, Address, MedicationNote
from .forms import AddNoteForm, AddInstructionNoteForm, SearchForUserForm, EditProfileForm, AddNotebookForm, AddCommunicationNoteForm, AddNoteReplyForm, UserProfileCreationForm, CreateProfessionalProfileForm, AddSelfCareNoteForm, AddResourceNoteForm, AddProcedureNoteForm, AddAppointmentNoteForm, AddContactNoteForm, AddMedicationNoteForm, UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm

# Displays and handles forms for user creation
def CreateNewUserView(request):
	if request.method == 'POST':
		user_form = UserCreationForm(request.POST, prefix='user_form')
		user_profile_form = UserProfileCreationForm(request.POST, request.FILES, prefix='user_profile_form')

		# Save new user if user_form is valid
		if user_form.is_valid():
			new_user = user_form.save()

			# Check if user_profile_form is valid and save variables to user profile
			if user_profile_form.is_valid():			
				medical_history = user_profile_form.cleaned_data['medical_history']
				phone_number = user_profile_form.cleaned_data['phone_number']
				title = user_profile_form.cleaned_data['title']
				profile_picture = user_profile_form.cleaned_data['profile_picture']
				first_name = user_profile_form.cleaned_data['first_name']
				last_name = user_profile_form.cleaned_data['last_name']

				# Address Information
				address_unit = user_profile_form.cleaned_data['address_unit']
				address_street = user_profile_form.cleaned_data['address_street']
				# address_city = user_profile_form.cleaned_data['address_city']
				# address_province = user_profile_form.cleaned_data['address_province']
				# address_country = user_profile_form.cleaned_data['address_country']
				# address_postal_code = user_profile_form.cleaned_data['address_postal_code']

				new_user_profile = UserProfile(user=new_user, address_street=address_street, address_unit=address_unit,
					address_city="Vancouver", address_province="BC", address_country="Canada",
					address_postal_code="V6K 3C8", medical_history=medical_history, phone_number=phone_number,
					title=title, profile_picture=profile_picture,
				)
				new_user_profile.save()

				# Login as new user
				username = user_form.cleaned_data['email']
				password = user_form.cleaned_data['password1']
				user = authenticate(username=username, password=password)
				login(request, user)

				# Save first and last name into user before loading template
				user.first_name = first_name
				user.last_name = last_name
				user.save()

				# Auto-add notebooks during account creation

				new_contact_notebook = Notebook(name='Contacts', description='Place all your contacts here',)
				new_contact_notebook.save()
				new_contact_notebook.editors.add(user)

				new_appointment_notebook = Notebook(name='Appointments', description='Place all your appointment notes here',)
				new_appointment_notebook.save()
				new_appointment_notebook.editors.add(user)

				new_medications_notebook = Notebook(name='Medications', description='Place all your medications here',)
				new_medications_notebook.save()
				new_medications_notebook.editors.add(user)

				new_notebook = Notebook(name='Notes', description='Place all your miscellaneous notes here',)
				new_notebook.save()
				new_notebook.editors.add(user)

				# Render addition form to fill out if professional
				if user_profile_form.cleaned_data['is_professional'] == True:
					return HttpResponseRedirect(reverse('create_professional'))

				# Return to dashboard if not professional
				return HttpResponseRedirect('/dashboard/')
	else:
		user_form = UserCreationForm(prefix='user_form')
		user_profile_form = UserProfileCreationForm(prefix='user_profile_form')
	return render(request, 'dashboard/create_user.html', {
		'user_form':user_form,
		'user_profile_form':user_profile_form,
	})

def CreateNewProfessionalView(request):
	if request.method == 'POST':
		form = CreateProfessionalProfileForm(request.POST)
		if form.is_valid():
			qualification = form.cleaned_data['qualification']
			job_title = form.cleaned_data['job_title']
			office_tel = form.cleaned_data['office_tel']
			office_email = form.cleaned_data['office_email']
			office_address = form.cleaned_data['office_address']
			
			# Get user and user profile
			user = request.user
			user_profile = user.user_profile

			# Save professional profile details
			user_profile.qualification = qualification
			user_profile.job_title = job_title
			user_profile.office_tel = office_tel
			user_profile.office_email = office_email
			user_profile.office_address = office_address
			user_profile.role = 'professional'

			# Save user profile
			user_profile.save()

			return HttpResponseRedirect('/dashboard/')
	else:
		form = CreateProfessionalProfileForm()
	return render(request, 'dashboard/create_user.html', {
		'form':form,
	})

# View for main dashboard
@login_required
def Dashboard(request):
	user = request.user
	return render(request, 'dashboard/index.html', {
		'user':user,
	})

# View for seeing profile's details
@login_required
def Profile(request):
	user = request.user
	user_profile = user.user_profile
	return render(request, 'dashboard/profile.html', {
		'user':user,
		'user_profile':user_profile,
		})

# View for profile edit 
@login_required
def EditProfile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']

			address_unit = form.cleaned_data['address_unit']
			address_street = form.cleaned_data['address_street']
			address_city = form.cleaned_data['address_city']
			address_province = form.cleaned_data['address_province']
			address_country = form.cleaned_data['address_country']
			address_postal_code = form.cleaned_data['address_postal_code']

			medical_history = form.cleaned_data['medical_history']
			phone_number = form.cleaned_data['phone_number']
			role = form.cleaned_data['role']
			title = form.cleaned_data['title']

			user = request.user
			user_profile = user.user_profile

			user.first_name = first_name
			user.last_name = last_name

			user_profile.address_unit = address_unit
			user_profile.address_street = address_street
			user_profile.address_city = address_city
			user_profile.address_province = address_province
			user_profile.address_country = address_country
			user_profile.address_postal_code = address_postal_code

			user_profile.medical_history = medical_history
			user_profile.phone_number = phone_number
			user_profile.role = role
			user_profile.title = title
			user_profile.profile_picture = request.FILES['profile_picture']

			user.save()
			user_profile.save()

			return HttpResponseRedirect(reverse('dashboard:profile'))
	else:
		form = EditProfileForm()
	return render(request, 'dashboard/edit_profile.html', {
		'form':form,
	})

@login_required
def CollaborationView(request):
	user = request.user
	user_profile = user.user_profile
	associates = user_profile.associates.all()
	notes = user.notes_read_write.all()
	notebooks_read_write = user.notebooks_read_write.all()
	notebooks_read_only = user.notebooks_read_only.all()

	return render(request, 'dashboard/collaboration.html', {
		'associates':associates,
		'notes':notes,
		'notebooks_read_only':notebooks_read_only,
		'notebooks_read_write':notebooks_read_write,
	})

# View for clinic's associated with user
@login_required
def ClinicView(request):
	user = request.user
	clinics = user.clinics.all()

	return render(request, 'dashboard/clinics.html', {
		'clinics':clinics,
		})

# View for viewing all notes and notebooks
@login_required
def NotesView(request):
	user = request.user
	authored_notes = user.authored_notes.filter(date_accessed__lte=timezone.now()).order_by('-date_accessed')[:10]
	notes_read_write = user.notes_read_write.filter(date_accessed__lte=timezone.now()).order_by('-date_accessed')[:10]
	notes_read_only = user.notes_read_only.filter(date_accessed__lte=timezone.now()).order_by('-date_accessed')[:10]

	notebooks_read_only = user.notebooks_read_only.all()
	notebooks_read_write = user.notebooks_read_write.all()

	return render(request, 'dashboard/notes.html', {
		'notes_read_write':notes_read_write,
		'notes_read_only':notes_read_only,
		'authored_notes':authored_notes,
		'notebooks_read_only':notebooks_read_only,
		'notebooks_read_write':notebooks_read_write,
	})

# View for selecting type of note to add
@login_required
def NotesSelectView(request):
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/note_select.html', {
		'notebook_id':notebook_id,
	})

@login_required
def AddGeneralNoteView(request):
	if request.method == 'POST':
		form = AddNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']

			new_note = Note(subject=subject, note_type='general_note',
				note_content=note, date_created=timezone.now(), date_accessed=timezone.now(),
				author=user)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)
			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_general_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddInstructionNoteView(request):
	if request.method == 'POST':
		form = AddInstructionNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			
			if form.is_valid():
				instructions = form.cleaned_data['instructions']
				new_note = InstructionNote(subject=subject, note_type='instruction_note', 
					note_content=note, date_created=timezone.now(), 
					date_accessed=timezone.now(), instructions=instructions, author=user,)

				# Optional parameters to be added to new_note object
				if form.cleaned_data['url'] != '':
					new_note.url = form.cleaned_data['url']
				if form.cleaned_data['follow_up'] != '':
					new_note.follow_up = form.cleaned_data['follow_up']

				new_note.save()

				# If user uploaded an attachment, relate it to the new note
				if request.FILES.get('attachment') != None:
					attachment = Attachment(file_attachment=request.FILES['attachment'])
					new_note.attachments.add(attachment)

				# If list of users was in post request, add them to note
				if 'choices_for_editors' in form.cleaned_data:
					for user in form.cleaned_data['choices_for_editors']:
						user = User.objects.get(username=user)
						user.notes_read_write.add(new_note)
				if 'choices_for_viewers' in form.cleaned_data:
					for user in form.cleaned_data['choices_for_viewers']:
						user = User.objects.get(username=user)
						user.notes_read_only.add(new_note)

				# If note is to be created in notebook, add note into notebook
				if 'notebook_id' in request.POST:
					notebook_id = request.POST['notebook_id']
					notebook = get_object_or_404(Notebook, pk=notebook_id)
					notebook.notes.add(new_note)

				request.user.authored_notes.add(new_note)
				return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddInstructionNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_instruction_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddCommunicationNoteView(request):
	if request.method == 'POST':
		form = AddCommunicationNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']

			importance = form.cleaned_data['importance']
			doctor = form.cleaned_data['choice_for_doctor']
			clinic = form.cleaned_data['choice_for_clinic']

			new_note = CommunicationNote(subject=subject, note_type='communication_note', 
				note_content=note, date_created=timezone.now(), date_accessed=timezone.now(), author=user, 
				importance=importance, doctor=doctor.user, clinic=clinic)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)
			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddCommunicationNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_communication_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddProcedureNoteView(request):
	if request.method == 'POST':
		form = AddProcedureNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			note_type = 'procedure_note'

			procedure = form.cleaned_data['procedure']
			weight = form.cleaned_data['weight']
			self_care_instructions = form.cleaned_data['self_care_instructions']
			emergency_instructions = form.cleaned_data['emergency_instructions']
			pre_procedure_instructions = form.cleaned_data['pre_procedure_instructions']
			follow_up_instructions = form.cleaned_data['follow_up_instructions']
			doctor = form.cleaned_data['choice_for_doctor']
			clinic = form.cleaned_data['choice_for_clinic']

			new_note = ProcedureNote(subject=subject, note_type=note_type, note_content=note, author=user, 
				procedure=procedure, weight=weight, self_care_instructions=self_care_instructions, 
				emergency_instructions=emergency_instructions, pre_procedure_instructions=pre_procedure_instructions, 
				follow_up_instructions=follow_up_instructions, doctor=doctor.user, clinic=clinic
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)
			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddProcedureNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_procedure_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddSelfCareNoteView(request):
	if request.method == 'POST':
		form = AddSelfCareNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note_content = form.cleaned_data['note_content']
			note_type = 'self_care_note'

			description = form.cleaned_data['description']
			frequency = form.cleaned_data['frequency']
			emergency_procedure = form.cleaned_data['emergency_procedure']
			procedure = form.cleaned_data['procedure']
			outcome = form.cleaned_data['outcome']
			date_and_time = form.cleaned_data['date_and_time']

			new_note = SelfCareNote(subject=subject, note_type=note_type, note_content=note_content, 
				author=user, description=description, emergency_procedure=emergency_procedure, 
				frequency=frequency, procedure=procedure, outcome=outcome, date_and_time=date_and_time,
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)

			# Recurring notes
			if frequency != 'not_repeating':
				if frequency == 'every_day':
					time_to_add = datetime.timedelta(days=1)
				if frequency == 'every_week':
					time_to_add = datetime.timedelta(weeks=1)
				if frequency == 'every_month':
					time_to_add = datetime.timedelta(days=30)
				
				# Create additional notes for recurring note
				end_date = form.cleaned_data['end_date']
				recurring_date = date_and_time
				recurring_date = recurring_date + time_to_add
				while recurring_date < end_date:
					new_note.pk = None
					new_note.id = None
					new_note.date_and_time = recurring_date
					new_note.save()
					recurring_date = recurring_date + time_to_add

			# URL for redirect to newly created note's detail page
			redirect_url = reverse('dashboard:note_detail', kwargs={'note_id': new_note.id})
			# Redirecting to note detail
			return HttpResponseRedirect(redirect_url + '?note_type=self_care_note')
	else:
		form = AddSelfCareNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_self_care_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddResourceNoteView(request):
	if request.method == 'POST':
		form = AddResourceNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			note_type = 'resource_note'

			doctor = form.cleaned_data['choice_for_doctor']
			clinic = form.cleaned_data['choice_for_clinic']

			new_note = ResourceNote(subject=subject, note_type=note_type, note_content=note, author=user, 
				doctor=doctor.user, clinic=clinic,
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)
			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddResourceNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_resource_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddAppointmentNoteView(request):
	if request.method == 'POST':
		form = AddAppointmentNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			note_type = 'appointment_note'

			reason_for_visit = form.cleaned_data['reason_for_visit']
			date_and_time = form.cleaned_data['date_and_time']
			doctor = form.cleaned_data['choice_for_doctor']
			clinic = form.cleaned_data['choice_for_clinic']
			frequency = form.cleaned_data['frequency']

			new_note = AppointmentNote(subject=subject, note_type=note_type, note_content=note, author=user, 
				doctor=doctor.user, clinic=clinic, reason_for_visit=reason_for_visit, date_and_time=date_and_time,
				frequency=frequency, 
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)

			# Recurring notes
			if frequency != 'not_repeating':
				if frequency == 'every_day':
					time_to_add = datetime.timedelta(days=1)
				if frequency == 'every_week':
					time_to_add = datetime.timedelta(weeks=1)
				if frequency == 'every_month':
					time_to_add = datetime.timedelta(days=30)
				
				# Create additional notes for recurring note
				end_date = form.cleaned_data['end_date']
				recurring_date = date_and_time
				recurring_date = recurring_date + time_to_add
				while recurring_date < end_date:
					new_note.pk = None
					new_note.id = None
					new_note.date_and_time = recurring_date
					new_note.save()
					recurring_date = recurring_date + time_to_add

			# URL for redirect to newly created note's detail page
			redirect_url = reverse('dashboard:note_detail', kwargs={'note_id': new_note.id})
			# Redirecting to note detail
			return HttpResponseRedirect(redirect_url + '?note_type=appointment_note')
	else:
		form = AddAppointmentNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_appointment_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddContactNoteView(request):
	if request.method == 'POST':
		form = AddContactNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			note_type = 'contact_note'

			unit = form.cleaned_data['unit']
			street = form.cleaned_data['street']
			city = form.cleaned_data['city']
			province = form.cleaned_data['province']
			country = form.cleaned_data['country']
			postal_code = form.cleaned_data['postal_code']

			address = Address(street=street, unit=unit, city=city, province=province, country=country,
				postal_code=postal_code
			)

			address.save()

			title = form.cleaned_data['title']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			organization_name = form.cleaned_data['organization_name']
			phone_number_work = form.cleaned_data['phone_number_work']
			phone_number_home = form.cleaned_data['phone_number_home']
			email = form.cleaned_data['email']

			new_note = ContactNote(address=address, subject=subject, note_type=note_type, note_content=note, author=user, 
				title=title, first_name=first_name, last_name=last_name, organization_name=organization_name,
				phone_number_work=phone_number_work, email=email
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)
			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = AddContactNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_contact_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

@login_required
def AddMedicationNoteView(request):
	if request.method == 'POST':
		form = AddMedicationNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']
			note_type = 'medication_note'

			unit = form.cleaned_data['unit']
			street = form.cleaned_data['street']
			city = form.cleaned_data['city']
			province = form.cleaned_data['province']
			country = form.cleaned_data['country']
			postal_code = form.cleaned_data['postal_code']

			address = Address(street=street, unit=unit, city=city, province=province, country=country,
				postal_code=postal_code
			)

			address.save()

			medication_name = form.cleaned_data['medication_name']
			medication_dosage = form.cleaned_data['medication_dosage']
			medication_frequency = form.cleaned_data['medication_frequency']
			medication_duration = form.cleaned_data['medication_duration']
			pharmacy_name = form.cleaned_data['pharmacy_name']
			pharmacy_telephone = form.cleaned_data['pharmacy_telephone']
			date_and_time = form.cleaned_data['date_and_time']

			new_note = MedicationNote(pharmacy_address=address, subject=subject, note_type=note_type, 
				note_content=note, author=user, medication_name=medication_name, 
				medication_dosage=medication_dosage, medication_frequency=medication_frequency, 
				pharmacy_name=pharmacy_name, pharmacy_telephone=pharmacy_telephone, 
				date_and_time=date_and_time,
			)

			# Optional parameters to be added to new_note object
			if form.cleaned_data['url'] != '':
				new_note.url = form.cleaned_data['url']
			if form.cleaned_data['follow_up'] != '':
				new_note.follow_up = form.cleaned_data['follow_up']

			new_note.save()

			# If user uploaded an attachment, relate it to the new note
			if request.FILES.get('attachment') != None:
				attachment = Attachment(file_attachment=request.FILES['attachment'])
				new_note.attachments.add(attachment)

			# If list of users was in post request, add them to note
			if 'choices_for_editors' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_editors']:
					user = User.objects.get(username=user)
					user.notes_read_write.add(new_note)
			if 'choices_for_viewers' in form.cleaned_data:
				for user in form.cleaned_data['choices_for_viewers']:
					user = User.objects.get(username=user)
					user.notes_read_only.add(new_note)

			# If note is to be created in notebook, add note into notebook
			if 'notebook_id' in request.POST:
				notebook_id = request.POST['notebook_id']
				notebook = get_object_or_404(Notebook, pk=notebook_id)
				notebook.notes.add(new_note)

			request.user.authored_notes.add(new_note)

			# Recurring notes
			frequency = medication_frequency
			if frequency != 'not_repeating':
				if frequency == 'every_day':
					time_to_add = datetime.timedelta(days=1)
				if frequency == 'every_week':
					time_to_add = datetime.timedelta(weeks=1)
				if frequency == 'every_month':
					time_to_add = datetime.timedelta(days=30)
				
				# Create additional notes for recurring note
				end_date = form.cleaned_data['end_date']
				recurring_date = date_and_time
				recurring_date = recurring_date + time_to_add
				while recurring_date < end_date:
					new_note.pk = None
					new_note.id = None
					new_note.date_and_time = recurring_date
					new_note.save()
					recurring_date = recurring_date + time_to_add
			
			# URL for redirect to newly created note's detail page
			redirect_url = reverse('dashboard:note_detail', kwargs={'note_id': new_note.id})
			# Redirecting to note detail
			return HttpResponseRedirect(redirect_url + '?note_type=medication_note')
	else:
		form = AddMedicationNoteForm(request.user.id)
	# Pass notebook_id to POST handling
	if 'notebook_id' in request.GET:
		notebook_id = request.GET['notebook_id']
	else:
		notebook_id = ''
	return render(request, 'dashboard/add_medication_note.html', {
		'form': form, 
		'notebook_id':notebook_id,
	})

# View for note details
@login_required
def NoteDetail(request, note_id):
	# Get requested note type
	note_type_requested = request.GET['note_type']

	# Dictionary to match requested note type from GET with model
	note_type_dict = {
				'general_note': Note,
				'instruction_note': InstructionNote,
				'communication_note': CommunicationNote,
				'procedure_note': ProcedureNote,
				'self_care_note': SelfCareNote,
				'resource_note': ResourceNote,
				'appointment_note': AppointmentNote,
				'contact_note': ContactNote, 
				'medication_note': MedicationNote, 
	}

	note = get_object_or_404(note_type_dict[note_type_requested], pk=note_id)
	replies = note.replies.filter(date_created__lte=timezone.now()).order_by('-date_created')[:10]
	attachments = note.attachments.all()
	user = request.user

	# Check if user can access note
	if note.ifUserCanAccessNote(user.id):
		# update date accessed for note
		note.noteAccessedNow()
		return render(request, 'dashboard/note_detail.html', {
			'user':user,
			'note':note,
			'attachments':attachments,
			'replies':replies,
		})
	else:
		raise Http404("Note not found.")

# View for sharing notes
@login_required
def ShareNote(request, note_id):
	if 'email' in request.GET:
		form = SearchForUserForm(request.GET)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = get_object_or_404(User, username = email)
			note = get_object_or_404(Note, id=note_id)
			user.notes_read_write.add(note)

			return HttpResponseRedirect(reverse('dashboard:notes'))
	else:
		form = SearchForUserForm()

	return render(request, 'dashboard/share_note.html', {
		'form':form,
	})

@login_required
def AddNotebookView(request):
	if request.method == 'POST':
		form = AddNotebookForm(request.POST)
		if form.is_valid():
			notebook_name = form.cleaned_data['name']
			notebook_description = form.cleaned_data['description']

			# Create and save new notebook object
			new_notebook = Notebook(name=notebook_name, description=notebook_description)
			new_notebook = form.save(commit=False)
			new_notebook.save()
			form.save_m2m()

			# Add new notebook to current user's read-write notebooks
			user = request.user
			user.notebooks_read_write.add(new_notebook)

			# URL for redirect to newly create notebook's detail page
			redirect_url = reverse('dashboard:notebook_detail', kwargs={'notebook_id': new_notebook.id})

			# Redirecting to notebook detail
			return HttpResponseRedirect(redirect_url)
	else:
		form = AddNotebookForm()
	return render(request, 'dashboard/add_notebook.html', {
		'form':form
	})

@login_required
def NotebookDetail(request, notebook_id):
	notebook = get_object_or_404(Notebook, pk=notebook_id)
	notebook_editors = notebook.editors.all()
	notebook_viewers = notebook.viewers.all()
	notes_in_notebook = notebook.notes.all().order_by('-date_created')
	user = request.user
	author_array = []

	# Place array of user objects in author_array
	for note in notes_in_notebook:
		author_array.append(note.author)

	zipped_list = zip(notes_in_notebook, author_array)
	
	return render(request, 'dashboard/notebook_detail.html', {
			'notebook':notebook,
			'zipped_list':zipped_list,
			'editors':notebook_editors,
	})

@login_required
def HealthToolsSearchResultsView(request):
	user = request.user
	query = request.GET['q']

	notebooks = user.notebooks_read_write.filter(Q(name__icontains=query) | Q(description__icontains=query))[:5]
	user_id = user.id

	# Query to get all notes that belong to user and contains search query in subject or contents
	notes = Note.objects.filter(Q(editors__id=user_id) | Q(viewers__id=user_id) | Q(author__id=user_id)).filter(Q(subject__icontains=query) | Q(note_content__icontains=query))[:10]

	return render(request, 'dashboard/health_tools_search_results.html', {
		'user':user,
		'notebooks':notebooks,
		'notes':notes,
	})

@login_required
def AddNotesToNotebookView(request, notebook_id):
	if request.method == 'POST':
		notebook = get_object_or_404(Notebook, pk=notebook_id)
		for key in request.POST:
			# If POST item is checkbox, get note from value and save to notebook
			if 'isChecked' in key:
				note_id = request.POST[key]
				note = get_object_or_404(Note, pk=note_id)
				notebook.notes.add(note)
		
		notebook.save()

		# URL for redirect to newly create notebook's detail page
		redirect_url = reverse('dashboard:notebook_detail', kwargs={'notebook_id': notebook_id})
		# Redirecting to notebook detail
		return HttpResponseRedirect(redirect_url)
	else:
		user = request.user
		notes = user.notes_read_write.all()
		notebook = get_object_or_404(Notebook, pk=notebook_id)

		# Grab notes not currently in notebook
		notes_not_in_notebook = []
		for note in notes:
			if note not in notebook.notes.all():
				notes_not_in_notebook.append(note)

		return render(request, 'dashboard/add_notes_to_notebook.html', {
			'notes':notes_not_in_notebook,
			'notebook_id':notebook_id,
		})

@login_required
def ShareNotebookView(request, notebook_id):
	if request.method == 'POST':
		notebook = get_object_or_404(Notebook, pk=notebook_id)
		for key in request.POST:
			if 'isChecked' in key:
				user_id = request.POST[key]
				user = get_object_or_404(User, pk=user_id)
				notebook.editors.add(user)
				notebook.save()

				message = "The notebook " + notebook.name + " was shared with you."
				notification = Notification(recipient=user, message=message)
				notification.save()

				# For each note in notebook, allow user to access
				for note in notebook.notes.all():
					note.editors.add(user)
					note.save()

		# URL for redirect to newly create notebook's detail page
		redirect_url = reverse('dashboard:notebook_detail', kwargs={'notebook_id': notebook_id})
		# Redirecting to notebook detail
		return HttpResponseRedirect(redirect_url)
	else:
		user = request.user
		user_profile = user.user_profile
		associates = user_profile.associates.all()
		notebook = get_object_or_404(Notebook, pk=notebook_id)

		# Grab notes not currently in notebook
		users_not_in_notebook = []
		for associate in associates:
			if associate.user not in notebook.editors.all():
				users_not_in_notebook.append(associate)

		return render(request, 'dashboard/share_notebook.html', {
			'associates':users_not_in_notebook,
			'notebook_id':notebook_id,
		})

@login_required
def SearchUserResultsView(request):
	searched_username = request.GET['u']
	search_results = []
	search_results = User.objects.filter(username__icontains = searched_username)

	return render(request, 'dashboard/user_search_results.html', {
		'search_results':search_results,
	})

@login_required
def PublicProfileView(request, user_id):
	public_profile_user = get_object_or_404(User, pk=user_id)
	associates = request.user.user_profile.associates.all()
	logged_in_user = request.user

	is_associate = logged_in_user.user_profile.is_associate(public_profile_user)

	return render(request, 'dashboard/public_profile.html', {
		'user':logged_in_user,
		'public_profile_user':public_profile_user,
		'is_associate':is_associate,
	})

@login_required
def AddAssociate(request, user_id):
	associate_to_add = get_object_or_404(User, pk=user_id)
	user = request.user
	user_profile = user.user_profile

	# For now, simply add as associate
	# To-Do - Send associate request and make message 'request sent'
	user_profile.associates.add(associate_to_add.user_profile)
	user_profile.save()
	
	# Notify user that he/she has been added as a team member
	message = user_profile.full_name() + " has added you as a team member."
	notification = Notification(recipient=associate_to_add, message=message)
	notification.save()
	
	is_associate = 1
	message = 'Associate added'

	return render(request, 'dashboard/public_profile.html', {
		'user':user,
		'public_profile_user':associate_to_add,
		'is_associate':is_associate,
		'message': message,
	})

def ClinicDetailView(request, clinic_id):
	clinic = get_object_or_404(Clinic, pk=clinic_id)

	return render(request, 'dashboard/clinic_detail.html', {
		'clinic':clinic,
	})

@login_required
def AddNoteReplyView(request, note_id):
	if request.method == 'POST':
		form = AddNoteReplyForm(request.POST)
		if form.is_valid():
			note = get_object_or_404(Note, pk=note_id)
			user = request.user
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']

			# Set and save the reply
			new_reply = NoteReply(note=note, title=title, content=content, author=user)
			new_reply.save()

			# URL for redirect back to note
			redirect_url = reverse('dashboard:note_detail', kwargs={'note_id': note_id})
			return HttpResponseRedirect(redirect_url + "?note_type=" + note.note_type)
	else:
		form = AddNoteReplyForm()
		return render(request, 'dashboard/add_note_reply.html', {
			'form':form,
			'note_id':note_id
		})

@login_required
def NotificationsView(request):
	user = request.user

	# Get 10 recent notifications
	read_notifications = user.notifications_received.filter(view_status__exact="read").filter(date_created__lte=timezone.now()).order_by('-date_created')[:5]
	unread_notifications = user.notifications_received.filter(view_status__exact="unread").filter(date_created__lte=timezone.now()).order_by('-date_created')[:5]

	return render(request, 'dashboard/notifications.html', {
		'user':user,
		'unread_notifications':unread_notifications,
		'read_notifications':read_notifications
	})

# Triggered by "Mark as Read" link on notification
@login_required
def MarkNotificationAsRead(request):
	notification = get_object_or_404(Notification, pk=request.GET['notification_id'])
	notification.view_status = 'read'
	notification.date_read = timezone.now()
	notification.save()

	return HttpResponseRedirect(reverse('dashboard:notifications'))

@login_required
def SchedulingView(request):
	user = request.user

	# Get all appointment, medication, and self care notes that belong to user and sort by date
	upcoming_tasks = Note.objects.filter(Q(editors__id=user.id) | Q(viewers__id=user.id) | Q(author__id=user.id))
	upcoming_tasks = upcoming_tasks.filter(Q(note_type__exact='appointment_note') | Q(note_type__exact='medication_note') | Q(note_type__exact='self_care_note'))
	upcoming_tasks = upcoming_tasks.filter(date_and_time__gte=timezone.now()).order_by('date_and_time')[:10]

	return render(request, 'dashboard/scheduling.html', {
		'upcoming_tasks':upcoming_tasks,
		'user':user, 	
	})

