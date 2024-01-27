from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from payment.models import Funds

class Property(models.Model):
    CHOICES_FOR_SELL_RENT = [
        ('For Sell', 'For Sell'),
        ('For Rent', 'For Rent'),
    ]

    CHOICES_PROPERTY_PURPOSE = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Building', 'Building'),
        ('Townhouse', 'Townhouse'),
        ('Home', 'Home'),
        ('Shop', 'Shop'),
        ('Office', 'Office'),
        ('Garage', 'Garage'),
    ]

    tag = models.CharField(max_length=20, choices=CHOICES_FOR_SELL_RENT)
    image = models.ImageField(upload_to='property_images/')
    purpose = models.CharField(max_length=20, choices=CHOICES_PROPERTY_PURPOSE)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    width_in_sqft = models.FloatField()
    no_of_bed = models.PositiveIntegerField(null=True, blank=True)
    no_of_bath = models.PositiveIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at'] 

    def __str__(self):
        return self.title

class PropertyStatus(models.Model):
    CHOICES_PROPERTY_STATUS = [
        ('Fast Growing', 'Fast Growing'),
        ('Hot Assets', 'Hot Assets'),
        ('Most Invested', 'Most Invested'),
    ]

    status = models.CharField(max_length=20, choices=CHOICES_PROPERTY_STATUS)
    investors_count = models.PositiveIntegerField()
    property = models.ManyToManyField(Property)

    class Meta:
        verbose_name_plural = "Property Statuses"
        ordering = ['status']

    def __str__(self):
        return self.status

class Investment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_percentage = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    account_type = models.CharField(max_length=20, choices=Funds.ACCOUNT_TYPES)  # Link to your existing Funds model

    class Meta:
        verbose_name_plural = "Investments"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Calculate interest_percentage based on the amount invested
        if self.amount >= 90000:
            self.interest_percentage = 50
        elif self.amount >= 40000:
            self.interest_percentage = 30
        else:
            self.interest_percentage = 15

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Investment of {self.user.username} in {self.property.title}"

class CloseInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50, default="TRC20")

    def __str__(self):
        return f"Closed Investment for {self.user.username} - {self.property.title} - {self.wallet_address}"

    class Meta:
        verbose_name_plural = "Closed Investments"
