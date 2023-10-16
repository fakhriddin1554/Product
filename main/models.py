from collections.abc import Iterable
from django.db import models
from blog.models import BaseModel
from authentication.models import CustomUser
from django.utils.text import slugify

class Person(models.Model):
    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=150, null=True)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=5, choices=GENDERS)
    nationality = models.CharField(max_length=50, default="Uzbek")
    is_married = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, verbose_name="Birth date")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name if self.last_name else ''}"


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    description = models.TextField(null=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to="products/%Y/%m/%d/", null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    


class Student(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=150, null=True)
    age = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name if self.last_name else ''}"
    

class Course(models.Model):
    title = models.CharField(max_length=100)
    students = models.ManyToManyField(to=Student)
    period = models.PositiveIntegerField(default=3)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title


class OrderProduct(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_products")
    quantity = models.PositiveBigIntegerField()

    def update_quantity(self):
        self.product.quantity -= self.quantity
        self.product.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.update_quantity()
        super(OrderProduct, self).save(self, *args, **kwargs)

class Order(BaseModel):
    NEW = 'new'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'

    ORDER_STATUS = (
        (NEW, 'New'),
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Conceled')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(choices=ORDER_STATUS, default=NEW, max_length=20)
    paid = models.BooleanField(default=False)