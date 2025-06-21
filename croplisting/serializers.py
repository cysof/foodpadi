from rest_framework import serializers
from .models import CropListing

class CropListingSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    img_url = serializers.SerializerMethodField()  # For Cloudinary image URL

    class Meta:
        model = CropListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'farmer']

    def get_img_url(self, obj):
        """
        Return the full Cloudinary image URL.
        """
        request = self.context.get('request')
        if obj.img and hasattr(obj.img, 'url'):
            return request.build_absolute_uri(obj.img.url) if request else obj.img.url
        return None

    def validate(self, attrs):
        """
        Ensure only FARMER users can create/update crop listings.
        """
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            user = request.user
            if not user.is_authenticated:
                raise serializers.ValidationError("Authentication is required.")
            if user.account_type != 'FARMER':
                raise serializers.ValidationError("Only users with Farmer account type can create or modify crop listings.")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['farmer'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['farmer'] = self.context['request'].user
        return super().update(instance, validated_data)
    

   