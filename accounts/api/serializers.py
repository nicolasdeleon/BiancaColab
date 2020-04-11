import hashlib
import random
from rest_framework import serializers

#modelo a serializar
from accounts.models import User, EmailConfirmed, Profile, Company


class RegistrationSerializer(serializers.ModelSerializer):

    # TODO: Hay que redifinir la forma en la que tomamos los campos
    # si vamos a usar un solo registrationSrializer para la empresa como para el usuario. 
    # Y hay que extraer campos de otros modelos.
    # Hay un ejemplo de como esta hecho esto en eventos/api/serializer: PostSerializer
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
        'role',
        'phone',
        'email',
        'first_name',
        'last_name',
        'instaaccount',
        'birth_date',
        'password',
        'password2',
        ]
        extra_kwargs = {
            "password" : {'write_only' : True}
        }

    def generateConfimationKey(self, user):
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(User=user)
        #Corro get or create lo que implica que email_is_created devuelve true siempre y cuando se genere bien
        #El mail se manda directamente de la funcion crear de EmailConfirmed class
        if email_is_created:
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8'))
            short_hash = short_hash.hexdigest()[:5]
            base, domain = str(User.email).split('@')
            activation_key = hashlib.sha1(str(short_hash+base).encode('utf-8')).hexdigest()
            email_confirmed.activation_key = activation_key
            # Un comment this comment the day we want to start using email validation on sign up and delete email_confirmed-confirmed = True
            # user.emailconfirmed.activate_user_email()
            email_confirmed.confirmed = True
            email_confirmed.save()

    def save(self):
        new_user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            role=self.validated_data['role'],
            phone=self.validated_data['phone'],
            staff=False,
            admin=False,
            active=True,
        )

        if(new_user.role == 1):
            user_profile = Profile(
                user=new_user,
                instaAccount=self.validated_data['instaaccount']
            )
            user_profile.save()

        elif (new_user.role == 2):
            user_company = Company(
                user=new_user,
                instaAccount=self.validated_data['instaaccount'],
                # TODO: Missing phone and company name
            )
            user_company.save()

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if(password != password2):
            raise serializers.ValidationError({'password:', 'Passwords must match'})
        name = self.validated_data['first_name'] + ' ' + self.validated_data['last_name']
        new_user.full_name = name
        new_user.set_password(password)
        # Generate EmailConfirmation
        new_user.save()
        self.generateConfimationKey(new_user)

        return new_user


class AccountPropertiesSerializer(serializers.ModelSerializer):
    # TODO: Esto habria que extenderlo a acout properties serializer para empresa y para usuario
    # colocando los campos pertinentes para cada uno utilizando la metodologia de
    # eventos/api/serializer: PostSerializer
    class Meta:
        model = User
        fields = ['email', 'full_name', 'instaaccount', 'birth_date']



class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
