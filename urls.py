
from django.urls import path
from .views import RegistrationView, LoginView, DashboardView, LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'), 
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
