from django.urls import path
from . import views

#Template urls set up app name variable
app_name='basic_app'

urlpatterns = [
    path('register/', views.register,name='register'),
    path('user_login/', views.user_login,name='user_login')
]
