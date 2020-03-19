# In any authentication related app create new file email_authentication_backends.py
from django.contrib.auth.models import  User
from django.contrib.auth.backends import ModelBackend

class EmailAuthBackend(ModelBackend):
	"""
	Extends default django ModelBackend for both Email Authentication and Username 
	Authentication against settings.AUTH_USER_MODEL 
	
	i.e: user can login with either email or username.
	
	"""
	def authenticate(self, request, username=None, password=None, **kwargs):
		if username is None:
			username = kwargs.get('username')
		try:
			print(username)
			user = User.objects.get(email=username)
		except User.DoesNotExist:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a non-existing user
			User().set_password(password)

		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
				