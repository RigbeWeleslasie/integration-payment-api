from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=28)

class Tag(models.Model):

     name=models.CharField(max_length=28)
class Product(models.Model):
    name=models.CharField(max_length=50)
    Category=models.ForeignKey(Category,null=True,on_delete=models.PROTECT)
    tags=models.ManyToManyField(Tag,blank=True)
    description=models.TextField()
    price=models.DecimalField(max_digits=4,decimal_places=2)
    stock=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name},price{self.price}"


    

class Subscription(models.Model):
    name=models.CharField(max_length=50)
class Customer(models.Model):
    Subscription=models.OneToOneField(Subscription,on_delete=models.CASCADE)



