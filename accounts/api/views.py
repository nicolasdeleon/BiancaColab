from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.views import APIView
from django.contrib.auth import authenticate

from accounts.models import User
from BarEvento.models import BarPost
from accounts.api.serializers import RegistrationSerializer, AccountPropertiesSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

##Cosas para manejar mail
import os
import smtplib


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

#Obtengo las credenciales ya verificadas del mail configurado para mandar mails
EMAIL_ADDRESS = "ndeleon@biancaapp.com"
EMAIL_PASSWORD = 'Delion47921'

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def send_feedback_view(request):
	context = {}
	#CHECK QUE EFECTIVAMENTE ESTA MI USER
	try:
		user = request.user
	except User.DoesNotExist:
		context['response'] = 'Error'
		context['error_message'] = 'User does not exist'
		return Response(context,status=status.HTTP_404_NOT_FOUND)
	
	#Tengo mi user
	with smtplib.SMTP('smtp.gmail.com',587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		
		smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

		subject = "HOla"
		body = f'{user.full_name} te manda un saludo'

		msg = f'Subject: {subject}\n\n{body}'
		context['Mensaje Enviado'] = msg
		context['Enviado desde'] = EMAIL_ADDRESS
		context['Enviado a'] = EMAIL_ADDRESS
		context['User'] = user.full_name

		smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,msg)
	return Response(context)