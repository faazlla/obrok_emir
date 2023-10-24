from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
import string

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.restaurant_name} {self.city} {self.address}"

    def generate_random_code(self, length=10):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    def add_funds(self, amount):
        self.available_funds += amount
        self.code = self.generate_random_code()  # Generisanje novog koda
        self.save()
        

    def subtract_funds(self, amount):
        if self.available_funds >= amount:
            self.available_funds -= amount
            self.code = self.generate_random_code()  # Generisanje novog koda
            self.save()
            return True  # Transakcija uspešna
        else:
            return False  # Nema dovoljno sredstava za transakciju




class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('obrok.Restaurant', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_time = models.DateTimeField(default=timezone.now)

class NewsItem(models.Model):
    NEWS_TYPES = (
        ('donation', 'Donation'),
        ('restaurant', 'Restaurant'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_type = models.CharField(max_length=20, choices=NEWS_TYPES)
    restaurant = models.ForeignKey('obrok.Restaurant', on_delete=models.CASCADE, related_name='news_items')
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    
