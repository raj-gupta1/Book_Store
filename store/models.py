from django.db import models
import datetime

# Create your models here.
#use of pillow


class Category(models.Model):
    name = models.CharField(max_length=100)


    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200,default='',null=True,blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=7)
    author = models.CharField(max_length=20)
    payment = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_products_by_id(category_id):
        if category_id:

            return Product.objects.filter(category=category_id)

        else:
            return Product.get_all_products()
    @staticmethod
    def get_products(ids):
        return Product.objects.filter(id__in=ids)

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def isExist(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price=models.IntegerField()
    address = models.CharField(max_length=100,default='',blank=True)
    phone=models.CharField(max_length=15,default='',blank=True)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default=False)
    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')


