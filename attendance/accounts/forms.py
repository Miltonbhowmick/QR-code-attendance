from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, CourseCode, ClassSession, StudentProfile, TeacherProfile
from django.db.models import Q
import re
import os

class RegistrationForm(forms.Form):

	POSITION_CHOICE = (
		(1,'Lecturer'),
		(2,'Asistant Professor'),
		(3,'Associate Professor'),
		(4,'Professor'),
	)

	DEPARTMENT = (
		(1,'Computer Science and Telecommunication Engineering'),
		(2,'Information and Communication Engineering'),
		(3,'Applied Chemistry and Chemical Engineering'),
		(4,'Applied Mathematics'),
	)
	user_type = forms.CharField(
		max_length= 20,
		help_text= 'Optional.',

		widget = forms.TextInput(
			attrs = {
				'class': 'form-control',
				'type': 'text',
				'name': 'teacher',
				'value': 'teacher',
				'readonly': 'readonly', 
			}
		)
	)
	username = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control',
					'type': 'text',
					'name': 'username',
					'placeholder': 'username',
				}
			)		
		)
	first_name = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control',
					'type': 'name',
					'name': 'first_name',
					'placeholder': 'first name',
				}
			)
		)
	last_name = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control', 
					'type': 'name',
					'name': 'last_name',
					'placeholder': 'last name',
			}
		)
	)
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control', 
					'type': 'email',
					'name': 'email',
					'placeholder': 'email',
			}
		)
	)
	password1 = forms.CharField(max_length=20, required=True, 

		widget = forms.PasswordInput(
			attrs = {
					'class': 'form-control', 
					'type': 'password',
					'name': 'password1',
					'placeholder': 'password',
			}
		)
	)
	password2 = forms.CharField(max_length=20, required=True,

		widget = forms.PasswordInput(
			attrs = {
					'class': 'form-control', 
					'type': 'password',
					'name': 'password2',
					'placeholder': 'confirm password',
			}
		)
	)
	teacher_position = forms.ChoiceField(widget=forms.RadioSelect, choices=POSITION_CHOICE)
	department = forms.ChoiceField(widget=forms.RadioSelect, choices=DEPARTMENT)

	def check_space(self, username):
		for x in username:
			if x == ' ':
				return True

		return False

	def clean(self):
		username = self.cleaned_data.get('username')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		teacher_position = self.cleaned_data.get('teacher_position')
		department = self.cleaned_data.get('department')
		if len(username) < 1:
			raise forms.ValidationError("Enter username!")
		else:
			check_username_space = self.check_space(username)

			if check_username_space:
				raise forms.ValidationError('You can not use space in username!')
			else:
				user_exist = User.objects.filter(username__iexact=username).exists()
				if user_exist:
					raise forms.ValidationError("Username already taken!")
				else:
					if len(email) < 1:
						raise forms.ValidationError("Enter email address!")
					else:
						email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)
						if email_correction == None:
							raise forms.ValidationError("Email not correct!")
						else:
							email_exist = User.objects.filter(email__iexact=email).exists()
							if email_exist:
								raise forms.ValidationError("Email already exist!")
							else:
								if len(password1) < 8:
									raise forms.ValidationError("Password is too short!")
								else:
									if password1 != password2:
										raise forms.ValidationError("Password not matched!")


	def deploy(self):
		DEPARTMENT = (
		(1,'Computer Science and Telecommunication Engineering'),
		(2,'Information and Communication Engineering'),
		(3,'Applied Chemistry and Chemical Engineering'),
		(4,'Applied Mathematics'),
		)
		username = self.cleaned_data.get('username')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		teacher_position = self.cleaned_data.get('teacher_position')
		department = self.cleaned_data.get('department')

		deploy1 = User(username=username, first_name=first_name, last_name=last_name, 
			email=email)
		deploy1.set_password(password1)
		deploy1.save()

		# print(deploy1)
		deploy2 = TeacherProfile(teacher_position= teacher_position)
		deploy2.teacher_user= deploy1
		deploy2.save()

		deploy3 = UserProfile.objects.get(user= deploy2.teacher_user)	
		department = int(department)
		deploy3.department = DEPARTMENT[department-1][department-1]
		deploy3.save()

# Additional information for users
class AdditionalInfoForm(forms.ModelForm):
	phone = forms.CharField(max_length=20, required = False)
	image = forms.ImageField( required = False)
	city = forms.CharField(max_length=50, required=False)
	country = forms.CharField(max_length=50, required=False)
	def clean(self):
		phone = self.cleaned_data.get('phone')
		image = self.cleaned_data.get('image')
		city = self.cleaned_data.get('city')
		country = self.cleaned_data.get('country')
		# if not phone:
		# 	raise forms.ValidationError('You have to write something!')
	class Meta:
		model = UserProfile
		fields = (
				'phone',
				'image',
				'city',
				'country',		
			)

# Registration form for students
class StudentSignUpForm(forms.Form):

	DEPARTMENT = (
		(1,'Computer Science and Telecommunication Engineering'),
		(2,'Information and Communication Engineering'),
		(3,'Applied Chemistry and Chemical Engineering'),
		(4,'Applied Mathematics'),
	)
	user_type = forms.CharField(
		max_length= 20,
		help_text= 'Optional.',

		widget = forms.TextInput(
			attrs = {
				'class': 'form-control',
				'type': 'text',
				'name': 'student',
				'value': 'student',
				'readonly': 'readonly', 
			}
		)
	)
	student_id = forms.CharField(
		max_length= 20,
		help_text= 'Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control',	
					'type': 'text',
					'name': 'student_id',
					'placeholder': 'student_id',
				}
		)	
	)
	username = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control',	
					'type': 'text',
					'name': 'username',
					'placeholder': 'username',
				}
			)		
		)
	first_name = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control',
					'type': 'name',
					'name': 'first_name',
					'placeholder': 'first name',
				}
			)
		)
	last_name = forms.CharField(
		max_length=30, 
		required=False, 
		help_text='Optional.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control', 
					'type': 'name',
					'name': 'last_name',
					'placeholder': 'last name',
			}
		)
	)
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',

		widget = forms.TextInput(
			attrs = {
					'class': 'form-control', 
					'type': 'email',
					'name': 'email',
					'placeholder': 'email',
			}
		)
	)
	password1 = forms.CharField(max_length=20, required=True, 

		widget = forms.PasswordInput(
			attrs = {
					'class': 'form-control', 
					'type': 'password',
					'name': 'password1',
					'placeholder': 'password',
			}
		)
	)
	password2 = forms.CharField(max_length=20, required=True,

		widget = forms.PasswordInput(
			attrs = {
					'class': 'form-control', 
					'type': 'password',
					'name': 'password2',
					'placeholder': 'confirm password',
			}
		)
	)
	student_session = forms.ModelChoiceField(queryset= ClassSession.objects.all(), to_field_name='session', required= False,
		)

	department = forms.ChoiceField(widget=forms.RadioSelect, choices=DEPARTMENT)

	# print(student_session)

	#class Meta:
	#	model = User
	#	fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

	def check_space(self, username):
		for x in username:
			if x == ' ':
				return True

		return False

	def clean(self):
		student_id = self.cleaned_data.get('student_id')
		username = self.cleaned_data.get('username')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		student_session = self.cleaned_data.get('student_session')
		department = self.cleaned_data.get('department')
	

		if len(username) < 1:
			raise forms.ValidationError("Enter username!")
		else:
			check_username_space = self.check_space(username)

			if check_username_space:
				raise forms.ValidationError('You can not use space in username!')
			else:
				user_exist = User.objects.filter(username__iexact=username).exists()
				if user_exist:
					raise forms.ValidationError("Username already taken!")
				else:
					if len(email) < 1:
						raise forms.ValidationError("Enter email address!")
					else:
						email_correction = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)
						if email_correction == None:
							raise forms.ValidationError("Email not correct!")
						else:
							email_exist = User.objects.filter(email__iexact=email).exists()
							if email_exist:
								raise forms.ValidationError("Email already exist!")
							else:
								if len(password1) < 8:
									raise forms.ValidationError("Password is too short!")
								else:
									if password1 != password2:
										raise forms.ValidationError("Password not matched!")

	def deploy(self):
		DEPARTMENT = (
			(1,'Computer Science and Telecommunication Engineering'),
			(2,'Information and Communication Engineering'),
			(3,'Applied Chemistry and Chemical Engineering'),
			(4,'Applied Mathematics'),
		)
		department = self.cleaned_data.get('department')
		student_id = self.cleaned_data.get('student_id')
		username = self.cleaned_data.get('username')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		student_session = self.cleaned_data.get('student_session')
		department = self.cleaned_data.get('department')
		
		deploy1 = User(username=username, first_name=first_name, last_name=last_name, 
			email=email)
		deploy1.set_password(password1)
		deploy1.save()

		# Converting roll no e.i 01,02,03.... from string value e.i ASH1511001M,BKH1511002F.....
		str_id = str(student_id)
		l = len(str_id)
		roll = str_id[l-3:l-1:1]
		roll= int(roll)

		deploy2 = StudentProfile(student_id = student_id, student_roll=roll, student_session= student_session)
		deploy2.student_user = deploy1
		deploy2.save()

		# user has been already saved sothat i call that user objects to store the data 
		deploy3 = UserProfile.objects.get(user= deploy2.student_user)	
		department = int(department)
		deploy3.department = DEPARTMENT[department-1][department-1]
		deploy3.save()


class EditProfileForm(UserChangeForm):
	class Meta:
		model =  User
		fields = {
			'email',
			'first_name',
			'last_name',
		}



