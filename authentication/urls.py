from django.urls import path
from .views import RegisterView, LogOutView,LoginView,ProfileView,DeleteUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/',LoginView.as_view(), name="login" ),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('delete/<int:pk>/', DeleteUser.as_view(), name="delete")

]