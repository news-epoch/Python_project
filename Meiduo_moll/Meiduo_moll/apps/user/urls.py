from django.conf.urls import include
from django.urls import path
from . import  views
app_name='user'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
]