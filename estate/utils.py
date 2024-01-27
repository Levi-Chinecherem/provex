from .models import Investment, Property, PropertyStatus, Investment
from datetime import datetime, timedelta
from django.utils import timezone
from payment.models import AccountSummary
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db import transaction  # Import transaction module

def make_investment(user, property_id, amount, account_type):
    # Handle the conversion to float gracefully
    try:
        amount = float(amount)
    except ValueError:
        # Handle the case where the conversion to float fails
        amount = 0.0  # Set a default value or handle the error appropriately

    property_obj = get_object_or_404(Property, pk=property_id)

    # Check if the user already has an investment in this property
    existing_investment = Investment.objects.filter(user=user, property=property_obj).first()

    if existing_investment:
        # Update the existing investment
        existing_investment.amount += Decimal(str(amount))
        existing_investment.created_at = timezone.now()
        existing_investment.save()

    else:
        # Check if there are sufficient funds in the AccountSummary for the given account_type
        account_summary = AccountSummary.objects.filter(user=user, account_type=account_type).first()

        if not account_summary or account_summary.total_amount < Decimal(str(amount)):
            # Not enough funds for the investment
            return None

        # Create a new investment
        investment = Investment.objects.create(
            user=user,
            property=property_obj,
            amount=amount,
            account_type=account_type
        )

        # Deduct the investment amount from the corresponding AccountSummary
        account_summary.total_amount -= Decimal(str(amount))
        account_summary.save()

        return investment

def get_user_investments(user):
    """Get all properties a user has invested in and their interests."""
    investments = Investment.objects.filter(user=user)
    user_investments = []

    for investment in investments:
        interest_percentage = investment.interest_percentage
        amount = float(investment.amount)  # Convert to float
        start_date = investment.created_at  # Assuming you have a 'created_at' field in your Investment model
        now = timezone.now()

        # Calculate future interest if investment is not up to a month
        future_interest = 0
        if (now - start_date).days < 30:
            future_interest = (interest_percentage / 100) * amount

        # Calculate current interest if investment is over a month
        current_interest = 0
        if (now - start_date).days >= 30:
            current_interest = (interest_percentage / 100) * amount

        # Append the investment object with additional information to the list
        investment.future_interest = future_interest
        investment.current_interest = current_interest
        user_investments.append(investment)

    return user_investments

def get_remaining_properties(user):
    """Get all properties that a user has not invested in."""
    all_properties = Property.objects.all()
    user_invested_properties = Investment.objects.filter(user=user).values_list('property', flat=True)
    remaining_properties = all_properties.exclude(id__in=user_invested_properties)
    return remaining_properties

def get_properties_by_status():
    """Get all properties grouped by their status."""
    property_status_dict = {}
    all_property_statuses = PropertyStatus.objects.all()
    for status in all_property_statuses:
        status_properties = Property.objects.filter(propertystatus=status)
        property_status_dict[status.status] = list(status_properties)
    return property_status_dict
