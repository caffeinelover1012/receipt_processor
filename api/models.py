import uuid
from django.db import models

class Item(models.Model):
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.short_description


class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    retailer = models.CharField(max_length=255)
    purchase_date = models.DateField()
    purchase_time = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.ManyToManyField(Item, related_name="receipts")

    def __str__(self):
        return f"{self.retailer} - {self.purchase_date}"
