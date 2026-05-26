from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT , default=1)
    
    def __str__(self):
        return self.title
    
    
    
class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.SmallIntegerField(default=1)

    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    class Meta:

        unique_together = ('user', 'menuitem')
        
    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} for {self.user.username}"


class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    delivery_crew = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='delivery_crew'
    )

    status = models.BooleanField(default=False)

    total = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.SmallIntegerField()

    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} for Order {self.order.id}"
