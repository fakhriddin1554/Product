from django.urls import path
from .views import index_page, about_page, contact_page,products

urlpatterns = [
    path('', index_page, name="index"),
    path('about/', about_page, name="about"),
    path('contact/', contact_page, name="contact"),
    path('category/<str:category>/', products, name="products")
]