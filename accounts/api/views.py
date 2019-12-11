from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.views import APIView
from django.contrib.auth import authenticate


from accounts.models import User
from BarEvento.models import BarPost
from accounts.api.serializers import RegistrationSerializer, AccountPropertiesSerializer, ChangePasswordSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([]) #Esto overridea mi settings default authentication

def api_registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email')
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		instaaccount = request.data.get('instaaccount')
		if validate_instaacount(instaaccount) != None:
			data['error_message'] = 'That instagram account is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if request.data.get('password') != request.data.get('password2'):
			data['error_message'] = 'Passwords must match'
			data['response'] = 'Error'
			return Response(data)

		if serializer.is_valid():
			user = serializer.save()
			data['response'] = 'user registered successfuly'
			data['email'] = user.email
			data['full_name'] = user.full_name
			data['active'] = user.active
			data['staff'] = user.staff
			data['admin'] = user.admin
			data['instaaccount'] = user.instaaccount
			data['timestamp'] = user.timestamp
			token = Token.objects.get(user=user).key
			data['token'] = token
		else:
			data = serializer.errors
			return Response(data)
		return Response(data)

def validate_email(email):
	user = None
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return None
	if user != None:
		return email

def validate_instaacount(instaaccount):
	user = None
	try:
		user = User.objects.get(instaaccount=instaaccount)
	except User.DoesNotExist:
		return None
	if user != None:
		return instaaccount

class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(email=email, password=password)
		if user:
			try:
				token = Token.objects.get(user=user)
				context['response'] = 'Successfully authenticated.'
				context['email'] = user.email
				context['token'] = token.key
			except Token.DoesNotExist:
				token = Token.objects.create(user=user)
				context['response'] = 'Successfully authenticated.'
				context['email'] = user.email
				context['full_name'] = user.full_name
				context['active'] = user.active
				context['staff'] = user.staff
				context['admin'] = user.admin
				context['instaaccount'] = user.instaaccount
				context['timestamp'] = user.timestamp
				context['token'] = token.key
		else:
			context['response'] = 'Error'
			##### TESTTTT: context['dataDeTest'] = str(request.data)
			context['error_message'] = 'Invalid credentials'
			return Response(context,status=status.HTTP_404_NOT_FOUND)
		return Response(context)


# Account properties
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
	context = {}
	try:
		user = request.user
	except User.DoesNotExist:
		context['response'] = 'Error'
		context['error_message'] = 'User does not exist'
		return Response(context,status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(user)
		return Response(serializer.data)

# Account update properties
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
	context = {}
	try:
		user = request.user
	except User.DoesNotExist:
		context['response'] = 'Error'
		context['error_message'] = 'User does not exist'
		return Response(context,status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(user, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = 'Account update success'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = User
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)