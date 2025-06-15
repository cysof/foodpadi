from rest_framework import serializers
from .models import CropListing

class CropListingSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)

    class Meta:
        model = CropListing
        fields = '__all__'
        read_only_fields = ['id','created_at', 'farmer']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            user = request.user
            if user.account_type != 'FARMER':
                raise serializers.ValidationError("Only users with Farmer account type can create or modify crop listings.")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)
