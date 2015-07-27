"""
Filename: views.py
Created on: June 13th, 2015th
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

from django.contrib.auth.models import User, Group
from dashboard.models import Clinic, Note, InstructionNote, Attachment, Notebook, CommunicationNote, DischargeNote, NoteReply
from .forms import AddNoteForm, AddInstructionNoteForm, SearchForUserForm, EditProfileForm, AddNotebookForm, AddCommunicationNoteForm, AddDischargeNoteForm, AddNoteReplyForm, CreateNewUserForm
from django.contrib.auth.forms import AdminPasswordChangeForm

def CreateNewUserView(request):
	if request.method == 'POST':
		pass
	else:
		form = CreateNewUserForm()
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
# Handles post request as well
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
		user = request.user
		user_profile = user.user_profile
		return render(request, 'dashboard/edit_profile.html', {
			'form':form,
			'user':user,	
			'user_profile':user_profile,
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

# View for adding a general note
@login_required
def AddNoteView(request):
	if request.method == 'POST':
		form = AddNoteForm(request.user.id, request.POST, request.FILES)
		if form.is_valid():
			user = request.user
			
			subject = form.cleaned_data['subject']
			note = form.cleaned_data['note_content']

			if request.POST['note_type'] == 'general_note':
				new_note = Note(subject=subject, note_type='general_note',
					note_content=note, date_created=timezone.now(), date_accessed=timezone.now(),
					author=user)
			
			if request.POST['note_type'] == 'instruction_note':
				form = AddInstructionNoteForm(request.user.id, request.POST,request.FILES)
				if form.is_valid():
					instructions = form.cleaned_data['instructions']
					new_note = InstructionNote(subject=subject, note_type='instruction_note', 
						note_content=note, date_created=timezone.now(), 
						date_accessed=timezone.now(), instructions=instructions, author=user,)

			if request.POST['note_type'] == 'communication_note':
				form = AddCommunicationNoteForm(request.user.id, request.POST,request.FILES)
				if form.is_valid():
					attention = form.cleaned_data['attention']
					importance = form.cleaned_data['importance']
					new_note = CommunicationNote(subject=subject, note_type='communication_note', 
						note_content=note, date_created=timezone.now(), 
						date_accessed=timezone.now(), author=user, attention=attention,
						importance=importance)		

			if request.POST['note_type'] == 'discharge_note':
				form = AddDischargeNoteForm(request.POST)
				if form.is_valid():

					procedure = form.cleaned_data['procedure']
					doctor = form.cleaned_data['doctor']
					weight = form.cleaned_data['weight']
					medication_dose = form.cleaned_data['medication_dose']
					next_dose = form.cleaned_data['next_dose']
					selfcare_instructions = form.cleaned_data['selfcare_instructions']
					emergency_instructions = form.cleaned_data['emergency_instructions']

					new_note = DischargeNote(subject=subject, note_type='discharge_note', 
						note_content=note, date_created=timezone.now(), 
						date_accessed=timezone.now(), author=user,procedure=procedure,
						doctor=doctor, medication_dose=medication_dose, next_dose=next_dose, weight=weight,
						selfcare_instructions=selfcare_instructions, emergency_instructions=emergency_instructions)		
			
			# Optional parameters to be added to new_note object
			if 'url' in form.cleaned_data:
				new_note.url = form.cleaned_data['url']
			if 'follow_up' in form.cleaned_data:
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
		if 'notebook_id' in request.GET:
			notebook_id = request.GET['notebook_id']
		else:
			notebook_id = ''

		if request.GET['note_type'] == 'general_note':
			form = AddNoteForm(request.user.id)
			return render(request, 'dashboard/add_general_note.html', {
				'form': form, 
				'notebook_id':notebook_id,
			})
		if request.GET['note_type'] == 'instruction_note':
			form = AddInstructionNoteForm(request.user.id)
			return render(request, 'dashboard/add_instruction_note.html', {
				'form': form, 
				'notebook_id':notebook_id,
			})
		if request.GET['note_type'] == 'communication_note':
			form = AddCommunicationNoteForm(request.user.id)
			return render(request, 'dashboard/add_communication_note.html', {
				'form': form, 
				'notebook_id':notebook_id,
			})
		if request.GET['note_type'] == 'discharge_note':
			form = AddDischargeNoteForm()
			return render(request, 'dashboard/add_discharge_note.html', {
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
				'discharge_note': DischargeNote,
	}

	note = get_object_or_404(note_type_dict[note_type_requested], pk=note_id)
	replies = note.replies.filter(date_created__lte=timezone.now()).order_by('-date_created')[:10]
	attachments = note.attachments.all()
	user = request.user

	# for note_user in note_users:
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
	is_associate = 1
	message = 'Associate added'

	return render(request, 'dashboard/public_profile.html', {
		'user':associate_to_add,
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
	notifications = user.notifications_received.all()

	return render(request, 'dashboard/notifications.html', {
		'user':user,
		'notifications':notifications,
	})
