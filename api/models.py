
# Create your models here.
from django.db import models
import random

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=150)
    image_url = models.TextField()

    def __str__(self):
        return self.name


class UPIInfo(models.Model):
    upi_id = models.CharField(max_length=100)
    payee_name = models.CharField(max_length=100)
    amount = models.IntegerField(default=150)
    qr_url = models.TextField()

    def __str__(self):
        return self.upi_id


class Batch(models.Model):
    batch_number = models.IntegerField(unique=True)
    approved_count = models.IntegerField(default=0)
    status = models.CharField(
        choices=[('open', 'Open'), ('full', 'Full'), ('drawn', 'Drawn')],
        default='open',
        max_length=10
    )
    winner_name = models.CharField(max_length=255, null=True, blank=True)
    winner_ticket_number = models.IntegerField(null=True, blank=True)
    drawn_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Batch {self.batch_number}"


class Submission(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    upi_reference = models.CharField(max_length=255, blank=True)

    payment_screenshot = models.TextField()  # base64 image

    selected_product = models.ForeignKey(Product, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.SET_NULL)
    ticket_number = models.IntegerField(null=True, blank=True)

    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)