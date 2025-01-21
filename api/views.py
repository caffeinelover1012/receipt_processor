from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReceiptSerializer
from .utils import calculate_points, prepare_receipt_data
from .models import Receipt, Item

class ReceiptProcessView(APIView):
    def post(self, request):
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            receipt_data = serializer.validated_data

            # Save the receipt and items to the database
            receipt = Receipt.objects.create(
                retailer=receipt_data["retailer"],
                purchase_date=receipt_data["purchaseDate"],
                purchase_time=receipt_data["purchaseTime"],
                total=receipt_data["total"],
            )

            for item in receipt_data["items"]:
                item_obj = Item.objects.create(
                    short_description=item["shortDescription"],
                    price=item["price"],
                )
                receipt.items.add(item_obj)

            receipt.save()
            return Response({"id": str(receipt.id)}, status=status.HTTP_200_OK)

        return Response(
            {"detail": "The receipt is invalid."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ReceiptPointsView(APIView):
    def get(self, request, id):
        try:
            # Fetch the receipt and related items from the database
            receipt = Receipt.objects.prefetch_related("items").get(id=id)

            # Prepare receipt data for point calculation
            receipt_data = prepare_receipt_data(receipt)

            # Calculate points
            points = calculate_points(receipt_data)

            # Return the calculated points
            return Response({"points": points}, status=status.HTTP_200_OK)
        except Receipt.DoesNotExist:
            # Handle case where the receipt ID is not found
            return Response({"detail": "No receipt found for that ID."}, status=status.HTTP_404_NOT_FOUND)

