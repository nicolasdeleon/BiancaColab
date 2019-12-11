from rest_framework import serializers

#modelo a serializar
from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True) #campo extra al form

    class Meta: #Requerido para mapear campos form a campos modelo
        model = User
        fields = ['email','full_name','instaaccount','password','password2']
        extra_kwargs = { #esta propiedad ni idea que hace
            "password" : {'write_only' : True}
        }

    def save(self):
        ObjUser = User(
            email = self.validated_data['email'],
		    instaaccount = self.validated_data['instaaccount'],
		    full_name = self.validated_data['full_name'],
		    staff = False,
		    admin = False,
		    active = True,
		)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if(password != password2):
            raise serializers.ValidationError({'password:','Passwords must match'})
        ObjUser.set_password(password)
        ObjUser.save()
        return ObjUser

class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta: #Requerido para mapear campos form a campos modelo
        model = User
        fields = ['email','full_name','instaaccount']


class ChangePasswordSerializer(serializers.Serializer):
    old_password                = serializers.CharField(required=True)
    new_password                = serializers.CharField(required=True)
    confirm_new_password        = serializers.CharField(required=True)