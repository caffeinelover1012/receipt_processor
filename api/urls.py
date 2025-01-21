from django.urls import path
from .views import ReceiptProcessView, ReceiptPointsView

urlpatterns = [
    path('receipts/process', ReceiptProcessView.as_view(), name='process-receipt'),
    path('receipts/<str:id>/points', ReceiptPointsView.as_view(), name='receipt-points'),
]
