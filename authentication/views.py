from django.shortcuts import render,redirect
from .forms import NewUserForm,ProfileUpdateForm
from django.views import View
from django.views.generic import DeleteView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile,CustomUser
from django.urls import reverse_lazy

class RegisterView(View):
    def get(self,request):
        form = NewUserForm
        return render(request, "auth/register.html", {"form":form})
    
    def post(self,request):
        form = NewUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request, "auth/register.html", {"form":form})
    

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "auth/login.html", {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
            
        return render(request, "auth/login.html", {"form": form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("index")
    

class ProfileView(View):
    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            form = ProfileUpdateForm(instance=profile)
            return render(request, "auth/profile.html", {"form":form})
        
    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            form = ProfileUpdateForm(data=request.POST, files=request.FILES, instance=profile)
            if form.is_valid():
                form.save()
            return redirect("index")
        

class DeleteUser(DeleteView):
    queryset = CustomUser.objects.all()
    template_name = "auth/delete.html"
    success_url = reverse_lazy("posts-list")