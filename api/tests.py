from api.serializers import ReceiptSerializer
from rest_framework.test import APITestCase
from rest_framework import status
import uuid

class ReceiptProcessorTests(APITestCase):
    def setUp(self):
        self.valid_receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
            }

        self.invalid_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [],
            "total": "9.00",
        }

    def test_process_receipt_valid(self):
        """Test that a valid receipt can be processed successfully."""
        response = self.client.post('/receipts/process', self.valid_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertTrue(uuid.UUID(response.data["id"]))

    def test_process_receipt_invalid(self):
        """Test that an invalid receipt returns a 400 status."""
        response = self.client.post('/receipts/process', self.invalid_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The receipt is invalid", response.data['detail'])

    def test_get_points_valid(self):
        """Test retrieving points for a valid receipt ID."""
        # First, process a valid receipt to generate an ID
        post_response = self.client.post('/receipts/process', self.valid_receipt, format='json')
        receipt_id = post_response.data["id"]

        # Retrieve points for the receipt ID
        get_response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertIn("points", get_response.data)
        self.assertIsInstance(get_response.data["points"], int)

    def test_get_points_invalid_id(self):
        """Test retrieving points for an invalid receipt ID."""
        invalid_id = str(uuid.uuid4())  # Generate a random, unused ID
        response = self.client.get(f'/receipts/{invalid_id}/points')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "No receipt found for that ID.")

    def test_points_calculation(self):
        """Test that points are calculated correctly based on the rules."""
        response = self.client.post('/receipts/process', self.valid_receipt, format='json')
        receipt_id = response.data["id"]

        # Retrieve points and validate calculation
        points_response = self.client.get(f'/receipts/{receipt_id}/points')
        points = points_response.data["points"]

        # Expected breakdown of points
        expected_points = 28
        self.assertEqual(points, expected_points)

    def test_multiple_receipts(self):
        """Test handling multiple receipts simultaneously."""
        # Process two different receipts
        receipt_1_response = self.client.post('/receipts/process', self.valid_receipt, format='json')
        receipt_2_response = self.client.post('/receipts/process', self.valid_receipt, format='json')

        # Retrieve points for each receipt
        id_1 = receipt_1_response.data["id"]
        id_2 = receipt_2_response.data["id"]

        points_1_response = self.client.get(f'/receipts/{id_1}/points')
        points_2_response = self.client.get(f'/receipts/{id_2}/points')

        self.assertEqual(points_1_response.status_code, status.HTTP_200_OK)
        self.assertEqual(points_2_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(id_1, id_2)
        self.assertEqual(points_1_response.data["points"], points_2_response.data["points"])

    def test_edge_case_empty_receipt(self):
        """Test submitting an empty payload."""
        response = self.client.post('/receipts/process', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edge_case_large_receipt(self):
        """Test processing a receipt with a large number of items."""
        large_receipt = self.valid_receipt.copy()
        large_receipt["items"] = [{"shortDescription": f"Item {i}", "price": "1.00"} for i in range(200)]

        response = self.client.post('/receipts/process', large_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        receipt_id = response.data["id"]

        points_response = self.client.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(points_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(points_response.data["points"], int)

    def test_receipt_serializer_valid(self):
        valid_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "total": "9.00",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
        }

        serializer = ReceiptSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors

    def test_receipt_serializer_invalid_items(self):
        invalid_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "total": "9.00",
            "items": [],
        }

        serializer = ReceiptSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert "items" in serializer.errors
