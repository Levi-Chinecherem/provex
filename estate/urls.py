from django.urls import path
from .views import dashboard, investments, other_assets, investment_details, property_details, assets, exchange, transfer

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('details/<int:property_id>/', property_details, name='property_details'),
    path('investments/', investments, name='investments'),
    path('investments/<int:investment_id>/', investment_details, name='investment_details'),
    path('other_assets/', other_assets, name='other_assets'),
    path('assets/', assets, name='assets'),
    path('exchange/', exchange, name='exchange'),
    path('transfer/', transfer, name='transfer'),
    # Add more paths as needed
]
