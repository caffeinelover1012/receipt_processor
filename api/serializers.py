from rest_framework import serializers
from .models import Receipt, Item

class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField(
        max_length=255, error_messages={
            "invalid": "The short description can only contain letters, numbers, spaces, and hyphens."
        }
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, error_messages={
            "invalid": "The price must be a valid decimal with two digits after the decimal point."
        }
    )

class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.CharField(
        max_length=255, error_messages={
            "invalid": "The retailer name can only contain letters, numbers, spaces, hyphens, and ampersands."
        }
    )
    purchaseDate = serializers.DateField()
    purchaseTime = serializers.TimeField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = ItemSerializer(many=True)

    def validate(self, data):
        # Ensure at least one item is included
        if len(data["items"]) == 0:
            raise serializers.ValidationError(
                {"items": "The receipt must contain at least one item."}
            )
        return data