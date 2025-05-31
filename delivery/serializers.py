from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_delivery_status(self, new_status):
        instance = self.instance
        if instance:
            current_status = instance.delivery_status
            valid_transitions = Delivery.VALID_DELIVERY_TRANSITIONS.get(current_status, [])
            if new_status not in valid_transitions and new_status != current_status:
                raise serializers.ValidationError(
                    f"Invalid transition from '{current_status}' to '{new_status}'."
                )
        return new_status

    def validate(self, attrs):
        # Optionally validate related objects or fields here
        return super().validate(attrs)
