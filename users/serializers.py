from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'birth', 'gender')

    # def validate(self, data):
    #     email = data.get('email', None)
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError('user already exists')
    #     return data

    # def create(self, validated_data):
    #     instance = User.objects.create(**validated_data)
    #     instance.email = validated_data.pop('email')
    #     instance.password = validated_data.pop('password')
    #     instance.username = validated_data.pop('username')
    #     instance.birth = validated_data.pop('birth')
    #     instance.gender = validated_data.pop('gender')
    #     return instance
    #
    # def update(self, instance, validated_data):
    #     instance.password = validated_data.get('password', instance.password)
    #     return instance
    #

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    # def validate(self, data):
    #     print('login_validate 진입')
    #     email = data.get('email', None)
    #     password = data.get('password', None)
    #     # user = User.objects.filter(email)
    #     # print('validate_email: ', email)
    #     # print('validate_password: ', password)
    #     # # print('user: ', user)
    #
    #     login = User(email=email, password=password)
    #     serializer = LoginSerializer(login)
    #     print(serializer.data)
    #     #
    #     # users_info = User.objects.all()
    #     # if email not in users_info:
    #     #     raise ValidationError('해당 아이디는 존재하지 않습니다.')
    #     # return data
    #     # if user not in data:
    #     #     raise ValidationError('해당 아이디는 존재하지 않습니다.')
    #     # return data

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']






