import requests
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required

categories = requests.get("https://dummyjson.com/products/categories").json()
context = {"categories": categories}

def index_page(request):
    now = datetime.now()
    return render(request, "main/index.html", context=context)

def about_page(request):
    return render(request, "main/about.html", context)

def contact_page(request):
    return render(request, "main/contact.html", context)

@login_required(login_url="/auth/login/")
def products(request, category):
    url = f"https://dummyjson.com/products/category/{category}"
    response = requests.get(url).json()
    products = response.get("products")
    return render(request, "main/products.html", context={"products":products, "categories":categories})