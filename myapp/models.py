from django.db import models
from django.contrib.auth.models import User


class product(models.Model):
    CATEGORY_CHOICES = [
        ('men', "Men's Wear"),
        ('women', "Women's Wear"),
        ('kids', "Kids' Wear"),
        ('accessories', "Accessories"),
        ('footwear', "Footwear"),
    ]

    pid = models.AutoField(primary_key=True)  # No comma here
    product_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    product_image = models.ImageField(upload_to='img/')
    product_title = models.CharField(max_length=200)
    product_description = models.CharField(max_length=1000)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_detail = models.TextField()  # Better for large text

    def __str__(self):
        return self.product_title

class Cart(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)  # For guest users
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # For logged-in users
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_title} - Qty: {self.quantity}"

    @property
    def total_price(self):
        return self.product.product_price * self.quantity
