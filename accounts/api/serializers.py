from rest_framework import serializers

#modelo a serializar
from accounts.models import user


class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True) #campo extra al form

    class Meta: #Requerido para mapear campos form a campos modelo
        model = user
<<<<<<< Updated upstream
        fields = ['email','full_name','instaaccount','password','password2']
=======
        fields = ['email',
        'first_name',
        'last_name',
        'instaaccount',
        birthDate,
        'birthDate',
        'password',
        'password2']
>>>>>>> Stashed changes
        extra_kwargs = { #esta propiedad ni idea que hace
            "password" : {'write_only' : True}
        }

    def save(self):
        ObjUser = user(
            email = self.validated_data['email'],
		    instaaccount = self.validated_data['instaaccount'],
<<<<<<< Updated upstream
		    full_name = self.validated_data['full_name'],
=======
		    first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            birthDate = self.validated_data['birthDate'],
>>>>>>> Stashed changes
		    staff = False,
		    admin = False,
		    active = True,
		)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if(password != password2):
            raise serializers.ValidationError({'password:','Passwords must match'})
        name = self.validated_data['first_name'] + ' ' + self.validated_data['last_name']
        ObjUser.set_full_name(name)
        ObjUser.set_password(password)
        ObjUser.save()
        return ObjUser

class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta: #Requerido para mapear campos form a campos modelo
        model = user
        fields = ['email','full_name','instaaccount','birthDate']


class ChangePasswordSerializer(serializers.Serializer):
    old_password                = serializers.CharField(required=True)
    new_password                = serializers.CharField(required=True)
    confirm_new_password        = serializers.CharField(required=True)