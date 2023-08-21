from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Admin Login Username- ecomm Pass-ecomm
# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=20)
    price = models.FloatField(default= 200)
    description = models.TextField()
    #size = models.FloatField(max_length=20)
    qty = models.IntegerField()
    image = models.ImageField(default= 'Abc.jpd', upload_to= 'Images')
    cat = models.ForeignKey(to= 'Category', on_delete=models.CASCADE)

    class Meta:
        db_table= "Product"

class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table= "Category"

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50,default=None)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)
    
class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateField(auto_now_add = True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment =models.ForeignKey(Payment,on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.price

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)