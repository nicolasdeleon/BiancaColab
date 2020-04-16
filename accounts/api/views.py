import binascii
import os
import random
import smtplib

from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializers import (AccountPropertiesSerializer,
                                      ChangePasswordSerializer,
                                      RegistrationSerializer)
from accounts.models import User,Profile,Company
from backBone_Bianca.settings import SUPPORT_EMAIL
import logging

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def api_registration_view(request):
    logger=logging.getLogger(__name__)
    if request.method == 'POST':
        data = {}
        email = request.data.get('email')
        role = request.data.get('role')
        if validate_email(email) is not None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        instaAccount = request.data.get('instaAccount')
        if validate_instaacount(instaAccount) is not None: # TODO: Hay que corregir la funcion validate_instaacount()
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
            if (role=='2'):
              company = Company(user=user,instaAccount=request.data.get('instaAccount'),phone=request.data.get('phone')).save()
            elif(role=='1'):
               if (request.data.get('phone') is None):
                 profile = Profile(user=user,instaAccount=request.data.get('instaAccount')).save()
               else:
                 profile = Profile(user=user,instaAccount=request.data.get('instaAccount'),phone=request.data.get('phone')).save()
            data['response'] = 'user registered successfuly'
            data['email'] = user.email
            data['full_name'] = user.full_name
            data['active'] = user.active
            data['staff'] = user.staff
            data['admin'] = user.admin
            data['instaAccount'] = instaAccount
            data['phone'] = request.data.get('phone')
            data['role'] = role         
            data['timestamp'] = user.timestamp
            token = Token.objects.get(user=user).key
            data['token'] = token
            logger.error(data)
        else:
            data = serializer.errors
            return Response(data)
        return Response(data, status=status.HTTP_201_CREATED)

def validate_email(email):
    user_aux = None
    try:        
        user_aux = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if User is not None:
        return email

def validate_instaacount(instaAccount):
    user_aux = None
    try:
        user_aux=Profile.objects.get(instaAccount=instaAccount)
        #user_aux = User.profile.get(instaAccount=instaaccount)
    except Profile.DoesNotExist:
        return None
    if Profile is not None:
        return instaAccount

class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.data.get('username')
        password = request.data.get('password')
        User = authenticate(email=email, password=password)
        if User:
            try:
                if User.emailconfirmed.confirmed:
                    token = Token.objects.get(user=User)
                    context['response'] = 'Successfully authenticated.'
                    context['email'] = User.email
                    context['token'] = token.key
                else:
                    context['error_message'] = f'Por favor, active su cuenta con el mail que a sido enviado a {User.email}'
            except Token.DoesNotExist:
                token = Token.objects.create(User=User)
                context['response'] = 'Usuario y/o contraseña inválida.'
                context['email'] = User.email
                context['full_name'] = User.full_name
                context['active'] = User.active
                context['staff'] = User.staff
                context['admin'] = User.admin
                #context['instaaccount'] = User.instaaccount
                context['timestamp'] = User.timestamp
                context['token'] = token.key
        else:
            context['error_message'] = 'Usuario y/o contraseña inválida.'
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        return Response(context)


# Account properties
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
    context = {}
    user = {}
    try:
        user = request.user
    except user.DoesNotExist:
        context['response'] = 'Error'
        context['error_message'] = 'User does not exist'
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
	    try:
	        profileAux = Profile.objects.get(user=user)
	        context['email'] = user.email        	
	        context['full_name'] = user.email
	        context['instaAccount'] = profileAux.instaAccount
	    except Profile.DoesNotExist:
	        context['response'] = 'Error'
	        context['error_message'] = 'Profile does not exist'
	        return Response(context, status=status.HTTP_404_NOT_FOUND)

    	
    #serializer = AccountPropertiesSerializer(user)
    return Response(context)

# Account update properties
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
    context = {}
    if request.method == 'PUT':
	    try:
        	user = request.user
        	profileAux = Profile.objects.get(user=user)
        	profileAux.instaAccount = request.data.get('instaAccount')
        	profileAux.save()
        	context['response'] = 'InstaAccount successfully changed'
        	return Response(context, status=status.HTTP_200_OK)

	    except User.DoesNotExist:
	    	context['response'] = 'Error'
	    	context['error_message'] = 'User does not exist'
	    	return Response(context, status=status.HTTP_404_NOT_FOUND)

    #if request.method == 'PUT':
    #    serializer = AccountPropertiesSerializer(User, data=request.data)
    #    data = {}
    #    if serializer.is_valid():
    #        serializer.save()
    #        data['response'] = 'Account update success'
    #        return Response(data=data)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.User
        return obj

    def update(self, request, *args, **kwargs):
        context = {}
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                context['response'] = 'Error'
                context['error_message'] = 'Contraseña actual errónea.'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:

                context['response'] = 'Error'
                context['error_message'] = 'Las nuevas contraseñas deben coincidir.'
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            context['response'] = 'OK'
            context['error_message'] = 'Contraseña cambiada con éxito.'
            return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


EMAIL_ADDRESS = "support@biancaapp.com"
EMAIL_PASSWORD = "Bianca3872"

@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def send_feedback_view(request):
    context = {}
    try:
        user = request.user
    except user.DoesNotExist:
        context['response'] = 'Error'
        context['error_message'] = 'User does not exist'
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    puntaje_promedio = request.data.get('puntaje_promedio')
    puntaje_fluidez = request.data.get('puntaje_fluidez')
    puntaje_atencion = request.data.get('puntaje_atencion')
    puntaje_pago = request.data.get('puntaje_pago')
    puntaje_general = request.data.get('puntaje_general')

    with smtplib.SMTP('smtp-relay.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        if puntaje_promedio <= 3:
            subject = f'Feedback, {User.full_name}, MAL'
        else:
            subject = f'Feedback, {User.full_name}, BIEN'

        body = f'{User.full_name} te te graduo asi..\nFluidez: {puntaje_fluidez}\nAtencion: {puntaje_atencion}\nPago: {puntaje_pago}\nGeneral: {puntaje_general}\nObteniendo un promedio: {puntaje_promedio}'
        msg = f'Subject: {subject}\n\n{body}'

        context['response'] = "Success"

        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
    return Response(context)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def reset_password(request):
    data = {}
    email = request.data.get('email')
    try:
        user_aux = User.objects.get(email=email)
        user_aux.reset_password_token = binascii.hexlify(os.urandom(6)).decode()[0:6]
        user_aux.save()

        subject = "Password Reset"
        context = {
            "reset_token": User_aux.reset_password_token
        }
        message = render_to_string("reset_password.html", context)

        from_email = SUPPORT_EMAIL

        mail = EmailMultiAlternatives(subject, from_email, [User_aux.email], '')
        mail.attach_alternative(message, "text/html")
        mail.send()

        data['response'] = "Success"
        return Response(data=data)
    except User.DoesNotExist:
        data['response'] = 'Error'
        data['error_message'] = 'No existe el usuario.'
        return Response(data)


@api_view(['POST', ])
@permission_classes((AllowAny, ))
def reset_password_confirm(request):
    data = {}
    email = request.data.get('email')
    token = request.data.get('token')
    password = request.data.get('password')
    try:
        user_aux = user.objects.get(email=email, reset_password_token=token)
        user_aux.set_password(password)
        user_aux.save()
        data["response"] = "Success"
        return Response(data=data)
    except user.DoesNotExist:
        data['response'] = 'Error'
        data['error_message'] = 'No existe el usuario.'
        return Response(data)

@api_view(['GET', ])
@permission_classes((AllowAny, ))
def get_accounts_general_info(request):
    data = {}

    number_of_users = len(User.objects.all())
    data['number_of_users'] = number_of_users
    return Response(data)
