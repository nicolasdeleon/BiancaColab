from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.views import APIView
from django.contrib.auth import authenticate


from accounts.models import user
from eventos.models import eventpost
from accounts.api.serializers import RegistrationSerializer, AccountPropertiesSerializer, ChangePasswordSerializer

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView

##Cosas para manejar mail
import os
import smtplib
import binascii
import random

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
		return Response(data,status=status.HTTP_201_CREATED)

def validate_email(email):
	user_aux = None
	try:
		user_aux = user.objects.get(email=email)
	except user.DoesNotExist:
		return None
	if user != None:
		return email

def validate_instaacount(instaaccount):
	user_aux = None
	try:
		user_aux = user.objects.get(instaaccount=instaaccount)
	except user.DoesNotExist:
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
	except user.DoesNotExist:
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
	except user.DoesNotExist:
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
	model = user
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
        
        
#Obtengo las credenciales ya verificadas del mail configurado para mandar mails
#EMAIL_ADDRESS = "nicolasmatiasdeleon@gmail.com" #ACA HAY Q PONER LA CUENTA DE SUPPORT DE BIANCA Y DARLE LOS PERMISOS CORRESPONDIENTES
#EMAIL_PASSWORD = 'bvbzvkelrbpbyegj'
EMAIL_ADDRESS = "support@biancaapp.com" 
EMAIL_PASSWORD = "Bianca3872"


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def send_feedback_view(request):
	context = {}
	#CHECK QUE EFECTIVAMENTE ESTA MI USER
	try:
		user = request.user
	except user.DoesNotExist:
		context['response'] = 'Error'
		context['error_message'] = 'User does not exist'
		return Response(context,status=status.HTTP_404_NOT_FOUND)
	
	puntaje_promedio = request.data.get('puntaje_promedio')
	puntaje_fluidez = request.data.get('puntaje_fluidez')
	puntaje_atencion = request.data.get('puntaje_atencion')
	puntaje_pago = request.data.get('puntaje_pago')
	puntaje_general = request.data.get('puntaje_general')
	
	#Tengo mi user
	with smtplib.SMTP('smtp-relay.gmail.com',587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		
		smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

		if(puntaje_promedio<=3):
			subject = f'Feedback, {user.full_name}, MAL'
		else:
			subject = f'Feedback, {user.full_name}, BIEN'
		
		body = f'{user.full_name} te te graduo asi..\nFluidez: {puntaje_fluidez}\nAtencion: {puntaje_atencion}\nPago: {puntaje_pago}\nGeneral: {puntaje_general}\nObteniendo un promedio: {puntaje_promedio}'
		msg = f'Subject: {subject}\n\n{body}'
		
		context['response'] = "Success"

		smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,msg)
	return Response(context)

#Obtengo las credenciales ya verificadas del mail configurado para mandar mails
EMAIL_ADDRESS2 = 'flororsi@gmail.com' #ACA HAY Q PONER LA CUENTA DE SUPPORT DE BIANCA Y DARLE LOS PERMISOS CORRESPONDIENTES
EMAIL_PASSWORD2 = 'ozdktmppasgklser'
'''
@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def reset_password(request):
	context = {}
	#CHECK QUE EFECTIVAMENTE ESTA MI USER
	try:
		user = request.user
	except User.DoesNotExist:
		context['response'] = 'Error'
		context['error_message'] = 'User does not exist'
		return Response(context,status=status.HTTP_404_NOT_FOUND)
	
	user.reset_password_token = binascii.hexlify(os.urandom(10)).decode()[0:10]
	user.save()

	#Tengo mi user
	with smtplib.SMTP('smtp.gmail.com',587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		
		smtp.login(EMAIL_ADDRESS2,EMAIL_PASSWORD2)

		subject = 'Password Reset'
		body = f'{user.full_name} tu clave de reseteo es: {user.reset_password_token}. \nPor favor colocarla en la aplicacion para su cambiar su password. \n\nSi usted no solicito el cambio de password por favor desestime el email.'
		msg = f'Subject: {subject}\n\n{body}'
		
		context['response'] = "Success"

		smtp.sendmail(user.email,user.email,msg)
	return Response(context)



class reset_password_confirm(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = user
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
			if not self.object.reset_password_token == serializer.data.get("old_password"):
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

'''
@api_view(['POST', ])
@permission_classes((AllowAny, ))
def reset_password(request):
	data={}
	email = request.data.get('email')
	try:
		user_aux = user.objects.get(email = email)
		#data["codeMail"] = "OK"
		user_aux.reset_password_token = binascii.hexlify(os.urandom(6)).decode()[0:6]
		user_aux.save()
		#Tengo mi user
		with smtplib.SMTP('smtp-relay.gmail.com',587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.ehlo()
			
			smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

			subject = 'Password Reset'
			body = f'{user_aux.full_name} tu clave de reseteo es:\n\n{user_aux.reset_password_token}\n\nIngresala en la app junto con la nueva password.\nSi no solicitaste el cambio de password desestimar el mail.'
			msg = f'Subject: {subject}\n\n{body}'
			
			data['response'] = "Success"

			smtp.sendmail(user_aux.email,user_aux.email,msg)
		return Response(data=data)
	except user.DoesNotExist:
		data['response'] = 'Error'
		data['error_message'] = 'User does not exist'
		#return Response(data,status=status.HTTP_404_NOT_FOUND)
		return Response(data)

@api_view(['POST', ])
@permission_classes((AllowAny, ))
def reset_password_confirm(request):
	data={}
	email = request.data.get('email')
	token = request.data.get('token')
	password = request.data.get('password')
	try:
		user_aux = user.objects.get(email = email, reset_password_token  = token)
		user_aux.set_password(password)
		user_aux.save()
		data["response"] = "Succes"
		return Response(data=data)
	except user.DoesNotExist:
		data['response'] = 'Error'
		data['error_message'] = 'User or token does not exist'
		#return Response(data,status=status.HTTP_404_NOT_FOUND)
		return Response(data)