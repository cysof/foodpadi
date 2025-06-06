from rest_framework import serializers
from .models import FarmPadiUser, Profile
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

class FarmPadiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmPadiUser
        fields = [
            'id', 'account_type', 'username', 'first_name', 'last_name', 'other_name',
            'gender', 'phone_number', 'email', 'address', 'city', 'state', 'country',
            'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')


class ProfileSerializer(serializers.ModelSerializer):
    user = FarmPadiUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=FarmPadiUser.objects.all(), source='user', write_only=True
    )
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_id', 'profile_type', 'profile_picture', 'date_of_birth']


class FarmPadiUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = FarmPadiUser
        fields = [
            'account_type', 'username', 'first_name', 'last_name', 'other_name',
            'gender', 'phone_number', 'email', 'address', 'city', 'state', 
            'country', 'password', 'password_confirm'
        ]
        extra_kwargs = {
            'phone_number': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'account_type': {'required': True},
            'gender': {'required': True},
            'address': {'required': True},
            'city': {'required': True},
            'state': {'required': True},
            'country': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_phone_number(self, value):
        if FarmPadiUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value

    def validate_email(self, value):
        if FarmPadiUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # REMOVED MANUAL PROFILE CREATION - Let the signal handle it
        user = FarmPadiUser.objects.create_user(
            password=password,
            **validated_data
        )
        # The signal will automatically create the profile
        return user


class FarmPadiUserDetailSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = FarmPadiUser
        fields = [
            'id', 'account_type', 'username', 'first_name', 'last_name', 
            'other_name', 'gender', 'phone_number', 'email', 'address', 
            'city', 'state', 'country', 'is_active', 'created_at', 
            'profile_picture'
        ]
        read_only_fields = ['id', 'created_at']

    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return obj.profile.profile_picture.url
        return None


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(
                request=self.context.get('request'),
                username=phone_number,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )

            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': FarmPadiUserSerializer(user).data
            }
        else:
            raise serializers.ValidationError(
                'Must include "phone_number" and "password".'
            )