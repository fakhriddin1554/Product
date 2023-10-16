from django.contrib import admin
from main.models import Product, Category, Order, OrderProduct

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)