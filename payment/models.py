from django.db import models
from django.contrib.auth.models import User
from store.models import Product
# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null =True, blank=True)
    shipping_fullname = models.CharField(max_length=255)
    shipping_email = models.EmailField()
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255,null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    #Dont Pluralise addrress
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address- {str(self.id)}'


#Create an order model 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null =True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField()
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=7 , decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'Order-{(str(self.id))}'


#Create orderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True) 
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)    
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

    quantity = models.PositiveBigIntegerField(default = 1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item- {str(self.id)}'

