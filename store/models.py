from uuid import uuid4
from django.db import models


class Promotion(models.Model):
    discription = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    discription = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE)
    promotion = models.ManyToManyField(Promotion,blank=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    message = models.TextField()
    

class Customer(models.Model):
    MEMBERSHIP_BRONZ='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZ,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZ)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering=['first_name','last_name']

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING,'Pending'),
        (PAYMENT_STATUS_FAILED,'Failed'),
        (PAYMENT_STATUS_COMPLETE,'Complete'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.IntegerField(max_length=6)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together=['cart','product']


