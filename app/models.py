from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MaxValueValidator
# Create your models here.
STATE_CHOICES= (
    ('Uttar pradesh' , 'Uttar pradesh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode= models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES , max_length=50)

    def __str__(self):
        return str(self.id) #id is default in every model class

CATEGORY_CHOICES = (
    ('M' , 'Mobile'),
    ('L' , 'Laptop'),
    ('TW' , 'TopWear'),
    ('BW' , 'BottomWear'),
)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price= models.IntegerField()
    discount_price= models.IntegerField()
    description = models.CharField(max_length=500)
    category = models.CharField(choices=CATEGORY_CHOICES , max_length=50)
    brand = models.CharField(max_length=100 , null=True)
    product_image = models.ImageField(null= True , blank= True , upload_to ='producting' )

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.PositiveBigIntegerField(default=1)

     def __str__(self):
        return str(self.id)

     @property
     def total_cost(self):
         return self.quantity * self.product.discount_price


STATUS_CHOICES = (
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Accepted','Accepted'),
    ('On The Way','On The Way'),
    ('Packed','Packed'),
)

class OrderedPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices= STATUS_CHOICES, max_length=10,  default='Pending')

    # Below Property will be used by orders.html page to show total cost
    @property
    def total_cost(self):
       return self.quantity * self.product.discount_price


