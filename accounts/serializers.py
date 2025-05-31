from rest_framework import serializers
from .models import FarmPadiUser, Profile

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
