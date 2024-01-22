from django.db import models

from products.models import Products
from users.models import User

class OrderitemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(null=True, blank=True)
    payment_on_get = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='In process')

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order № {self.pk} | Customer {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model): # ordered items by user
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150) # if product was deleted, just in case 
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date of sale")
    
    class Meta:
        db_table = "order_item"
        verbose_name = "Sold item"
        verbose_name_plural = "Sold items"

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Product name {self.name} | Order № {self.order.pk}"