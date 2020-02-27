import hashlib
import random
from rest_framework import serializers

#modelo a serializar
from accounts.models import user, EmailConfirmed


class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True) #campo extra al form

    class Meta: #Requerido para mapear campos form a campos modelo
        model = user
        fields = ['email',
        'first_name',
        'last_name',
        'instaaccount',
        'birth_date',
        'password',
        'password2']
        extra_kwargs = { #esta propiedad ni idea que hace
            "password" : {'write_only' : True}
        }
    
    def generateConfimationKey(self, user):
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        #Corro get or create lo que implica que email_is_created devuelve true siempre y cuando se genere bien
        #El mail se manda directamente de la funcion crear de EmailConfirmed class
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8'))
            short_hash = short_hash.hexdigest()[:5]
            base, domain = str(user.email).split('@')
            activation_key = hashlib.sha1(str(short_hash+base).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = activation_key
            # Un comment this comment the day we want to start using email validation on sign up and delete email_confirmed-confirmed = True
            # user.emailconfirmed.activate_user_email()
            email_confirmed.confirmed = True
            email_confirmed.save()

    def save(self):
        ObjUser = user(
            email = self.validated_data['email'],
            instaaccount = self.validated_data['instaaccount'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            birth_date = self.validated_data['birthDate'],
            staff = False,
            admin = False,
            active = True,
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if(password != password2):
            raise serializers.ValidationError({'password:','Passwords must match'})
        name = self.validated_data['first_name'] + ' ' + self.validated_data['last_name']
        ObjUser.full_name=name
        ObjUser.set_password(password)
        
        #Generate EmailConfirmation
        ObjUser.save()
        self.generateConfimationKey(ObjUser)

        return ObjUser

class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta: #Requerido para mapear campos form a campos modelo
        model = user
        fields = ['email','full_name','instaaccount','birth_date']


class ChangePasswordSerializer(serializers.Serializer):
    old_password                = serializers.CharField(required=True)
    new_password                = serializers.CharField(required=True)
    confirm_new_password        = serializers.CharField(required=True)