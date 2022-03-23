from rest_framework import serializers
from django.contrib.auth import authenticate
from contrib.email_validator import validate_email
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)
        read_only_fields = ('token',)

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta(object):
        model = User
        fields = ('email', 'first_name', 'username', 'last_name', 'password', 'token')

    def create(self, validated_data):
        if not validate_email(validated_data.get('email')):
            raise serializers.ValidationError(
                "This email can not be used"
            )
        
        return User.objects.create_user(**validated_data)

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 255)
    username = serializers.CharField(max_length = 255, read_only = True)
    password = serializers.CharField(max_length = 128, write_only = True)
    token = serializers.CharField(max_length = 255, read_only = True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email is required'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required'
            )
        
        #username = email because in the User model the constant USERNAME_FIELD is assigned as email
        #USERNAME_FIELD = email
        user = authenticate(username = email, password = password)
        
        if user is None:
            raise serializers.ValidationError(
              'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )
        return {
            'email' : user.email,
            'username' : user.username,
            'token' : user.token
        }
        
