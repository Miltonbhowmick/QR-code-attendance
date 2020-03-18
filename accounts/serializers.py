from rest_framework import serializers
from .models import UserProfile, StudentProfile, PresentSheet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class HelloSerializer(serializers.Serializer):
	""" Serializers a name field for testing out APIView """

	name = serializers.CharField(max_length= 10)

class LoginSerializer(serializers.Serializer):
	email = serializers.CharField()
	password = serializers.CharField()

	def validate(self,data):
		email = data.get("email", "")
		password = data.get("password","")

		if email and password:
			user = authenticate(username=email,password=password)
			if user:
				if user.is_active:
					data["user"] = user
				else:
					msg = "User is deactivated."
					raise serializers.ValidationError("User is deactivated.")
			else:
				msg = "Unable to login with given credentials."
				raise serializers.ValidationError("User is deactivated.")
		else:
			msg = "Must provide email and password both."
			raise serializers.ValidationError("User is deactivated.")
		return data

class UserProfileSerializer(serializers.ModelSerializer):
	""" A serializer for our user profile objects. """

	# username = serializers.CharField(source= user.username)	
	class Meta:
		model = User
		fields = ('username', 'email')

	def create(self, validated_data):
		""" Create and return a new user. """

		username = validated_data['username']
		email = validated_data['email']

		user = User(
			username = username,
			email = email,
		)

		user.set_password(validated_data['password'])
		user.save()

		return user

class StudentProfileSerializer(serializers.ModelSerializer):

	# collecting the serializers of all Users 
	student_user = UserProfileSerializer(required= True)
	# Creating fields for "StudentProfileSerializer" using Class Meta
	class Meta:
		model = StudentProfile
		fields = ('student_id','student_user', 'student_session')

	def create(self, validated_data):
		student_id = validated_data['student_id']
		user_data = validated_data['student_user']
		student_user = UserProfileSerializer.create(UserProfileSerializer(), validated_data['user_data'])
		student_session = validated_data['student_session']
		
		student, created = StudentProfile.objects.update_or_create(student_user=student_user, student_session= student_session)

		return student

class CoursePresentSheetSerializer(serializers.ModelSerializer):
	# attend_user = UserProfileSerializer(required =True)

	class Meta:
		model = PresentSheet
		fields = ( 'join_date','attend_user','select_course_code','select_session','random_url')




















