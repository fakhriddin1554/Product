from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Password',
        style={'input_type': 'password', 'placeholder': 'Password here'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Password Confirmation',
        style={'input_type': 'password', 'placeholder': 'Password Confirmation here'}
    )

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError({"password1":"Parollar bir xil emas","password2":"Parollar bir xil emas"})
        return attrs
    
    def create(self, validated_data):
        email = validated_data.get("email")
        phone = validated_data.get("phone")
        password = validated_data.get("password1")
        user = User.objects.create(email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user
    
    def get_token(self,user:User):
        token, created = Token.objects.get_or_create(user=user)
        return token

    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Password',
        style={'input_type': 'password', 'placeholder': 'Password here'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError({"email":"User doesn't exists"})
        return attrs

    def get_token(self, user: User):
        token, created = Token.objects.get_or_create(user=user)
        return token


    