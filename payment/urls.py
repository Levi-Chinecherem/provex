# payment/urls.py
from django.urls import path
from .views import add_funds, success_page

urlpatterns = [
    path('add_funds/', add_funds, name='add_funds'),
    path('success/', success_page, name='success_page'),
]
