from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
def __str__(self):
    return self.username


class Size(models.Model):
    name = models.CharField(max_length=50)
def __str__(self):
    return self.username


class Brands(models.Model):
    name = models.CharField(max_length=50)
def __str__(self):
    return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sku = models.CharField(max_length=50,unique=True,blank=True,null=True)
    tags = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to='products/',default='default.jpg',blank=True,null=True)
    ex_image1 = models.ImageField(upload_to='products/',default='default.jpg',blank=True,null=True)
    ex_image2 = models.ImageField(upload_to='products/',default='default.jpg',blank=True,null=True)
    ex_image3 = models.ImageField(upload_to='products/',default='default.jpg',blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    condition = models.CharField(max_length=50,choices=[('new','New'),('sale','Sale')])
    new_arrival = models.BooleanField(default=False)
    top_rated = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)

def __str__(self):
    return self.username


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    rating = models.IntegerField(blank=True,null=True)
    comment = models.TextField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)

def __str__(self):
    return f"{self.user}-{self.product.name}-{self.rating}"


class SliderItem(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider_images/')
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title

