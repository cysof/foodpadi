from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    crop_name = serializers.CharField(source='crop.crop_name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['ordered_at', 'updated_at', 'buyer', 'total_price', 'price_per_unit', 'status']

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            crop = attrs.get('crop')
            if crop and crop.farmer == request.user:
                raise serializers.ValidationError("You cannot order your own crop.")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)
