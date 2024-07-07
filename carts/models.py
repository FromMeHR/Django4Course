from django.db import models

from products.models import Products
from users.models import User

class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ("id",)
        
    objects = CartQueryset().as_manager() # + own methods to objects
        
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user: 
            return f'Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity}'
        return f'Anonymous cart | Product {self.product.name} | Quantity {self.quantity}'