from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
import uuid, os
import datetime

# Create your models here.

class CourseCode(models.Model):
	teacher1 = models.ForeignKey(User, related_name='teacher1', on_delete=models.CASCADE, null=True, blank=True)
	teacher2 = models.ForeignKey(User, related_name='teacher2', on_delete=models.CASCADE, null=True, blank=True)
	course_code = models.CharField(max_length= 50, blank=True)
	session = models.ForeignKey('ClassSession', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.course_code

class ClassSession(models.Model):
	session = models.CharField(max_length=50, default='')
	slug = models.SlugField(unique=True, blank=True)
	
	def __str__(self):
		return self.session

	def get_absolute_url(self):
		return reverse('accounts:session', args=[self.slug])

class UserProfile(models.Model):
	DEPARTMENT = (
		(1,'Computer Science and Telecommunication Engineering'),
		(2,'Information and Communication Engineering'),
		(3,'Applied Chemistry and Chemical Engineering'),
		(4,'Applied Mathematics'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length= 20, blank=True)
	image = models.ImageField(upload_to= 'profile_image', blank= True, null= True)
	# location fields 
	city = models.CharField(max_length= 50, blank=True)
	country = models.CharField(max_length = 50, blank=True)
	department = models.CharField(max_length = 50, blank=True)

	def __str__(self):
		name=self.user.username 
		return name


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class PresentSheet(models.Model):
	attend_user = models.ManyToManyField(User)
	join_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)
	select_course_code = models.CharField(max_length= 50, blank=True)
	select_session = models.CharField(max_length=50, blank= True)
	random_url = models.CharField(max_length=200, blank= True)
	""" Another method """
	# d = str(datetime.datetime.now().time())
	# d = d.replace(":","-")
	# d = d.replace(".","-")
	# join_date = "("+str(datetime.datetime.now().date()) +") ("+ d 
	""""""	
	def __str__(self):
		class_name = str(self.select_course_code) +" ("+ str(self.select_session) +") ("+(((str(self.join_date)).split(".")))[0]+")"	
		return class_name

	def get_absolute_url(self):
		return reverse('accounts:present_sheet',args=[self.random_url])

class TeacherProfile(models.Model):
	POSITION_CHOICE = (
		(1,'Lecturer'),
		(2,'Asistant Professor'),
		(3,'Associate Professor'),
		(4,'Professor'),
	)
	teacher_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	teacher_image = models.ImageField(upload_to = 'teachers/image', blank= True, null = True)
	teacher_position = models.CharField(max_length= 20, choices = POSITION_CHOICE)
	class_presentsheet = models.ManyToManyField(PresentSheet)

	user_type = models.CharField(max_length= 20, default='teacher')

	def __str__(self):
		return f'{self.teacher_user}'

class StudentProfile(models.Model):
	student_id = models.CharField(max_length=50, blank=True)
	student_roll = models.IntegerField(default=None)
	student_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	student_image = models.ImageField(upload_to= 'students/image', blank= True, null= True)
	student_session = models.CharField(max_length= 50)

	user_type = models.CharField(max_length= 20, default='student')

	def __str__(self):
		return f'{self.student_user}'

class CoursePercentage(models.Model):
	student_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	course_code = models.ForeignKey(CourseCode, on_delete=models.CASCADE, blank=True, null=True)
	session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, blank=True, null=True)
	percentage = models.IntegerField(null=True)

	teacher_user = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE,null=True)

	def __str__(self):
		return str(self.student_user.username)+" "+str(self.course_code)

