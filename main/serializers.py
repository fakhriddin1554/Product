from rest_framework import serializers
from .models import Category, Product

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "slug", "title", "description")
        read_only_fields = ("id", "slug")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "title","slug", "description", "price", "image", "quantity", "category", "created", "updated")
        read_only_fields = ("id", "slug", "created", "updated")