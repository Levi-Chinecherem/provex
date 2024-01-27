from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CloseInvestment, Property, PropertyStatus, Investment
from .utils import get_user_investments, get_remaining_properties, get_properties_by_status
from django.utils import timezone
from datetime import timedelta
from payment.utils import get_latest_usdt_trc20, get_latest_usdt_erc20, get_latest_btc, get_account_details
from payment.views import funds_details 
from .utils import make_investment

@login_required
def dashboard(request):
    user = request.user

    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Get all PropertyStatus items
    property_statuses = PropertyStatus.objects.all()

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'property_statuses': property_statuses,
    }

    return render(request, 'dashboard_T/dashboard.html', context)

@login_required
def property_details(request, property_id):
    user = request.user
    property_obj = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        account_type = request.POST.get('account_type')

        # Call the make_investment utility function
        investment = make_investment(user, property_id, amount, account_type)

        if investment:
            return redirect('investments')  # Redirect to the investments page or any other page you prefer

    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'property': property_obj,
    }

    return render(request, 'dashboard_T/property_details.html', context)

@login_required
def investments(request):
    user = request.user
    # Get all investments made by the logged-in user
    user_investments = get_user_investments(request.user)

    for investment in user_investments:
        print(f"Investment ID: {investment.id}")

    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'user_investments': user_investments,
    }

    return render(request, 'dashboard_L/investments.html', context)

@login_required
def investment_details(request, investment_id):
    user = request.user
    try:
        investment = get_object_or_404(Investment, pk=investment_id)

        if request.method == 'POST':
            wallet_address = request.POST.get('wallet_address')

            # Assuming you have a function to validate the wallet address
            if wallet_address:
                # Create a ClosedInvestment entry
                CloseInvestment.objects.create(
                    user=request.user,
                    property=investment.property,
                    wallet_address=wallet_address,
                    network="TRC20"  # You can adjust the network as needed
                )

                # Optionally, you can perform additional actions here

                # Redirect to a success page or return a response
                return redirect('dashboard')

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

        # Calculate future interest due date
        future_interest_due_date = investment.created_at + timedelta(days=30)

        # Calculate the number of days remaining for future interest
        days_remaining = (future_interest_due_date - timezone.now()).days

        # Calculate the number of days past the due date
        days_past_due = 30 + (timezone.now() - future_interest_due_date).days

        # Other useful insights can be calculated here based on your requirements

        # Fetch account balances and last four digits for each account type
        usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
        usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
        btc_details = get_account_details(user, 'BTC')

        # Create context
        context = {
            'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
            'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
            'btc_balance': btc_details['btc_balance'],
            'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
            'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
            'btc_last_digits': btc_details['btc_last_digits'],
            'investment': investment,
            'future_interest': future_interest,
            'current_interest': current_interest,
            'future_interest_due_date': future_interest_due_date,
            'days_remaining': days_remaining,
            'days_past_due': days_past_due,
            # Add more context variables as needed
        }

        return render(request, 'dashboard_L/investment_details.html', context)
    except Exception as e:
        print(f'Error in investment_details view: {e}')
        # Handle the exception or add more debugging information
        return render(request, 'dashboard_L/investment_details.html', {'error': 'An error occurred'})

@login_required
def other_assets(request):
    user = request.user
    # Get properties that the user has not invested in
    remaining_properties = get_remaining_properties(request.user)

    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'remaining_properties': remaining_properties,
    }
    
    return render(request, 'dashboard_L/other_assets.html', context)

@login_required
def assets(request):
    user = request.user
    # Get all properties 
    properties = Property.objects.all()

    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'properties': properties,
    }

    return render(request, 'dashboard_T/assets.html', context)

@login_required
def exchange(request):
    user = request.user
    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
    }

    return render(request, 'dashboard_T/exchange.html', context)

@login_required
def transfer(request):
    # Get the latest data from each model using the utility functions
    latest_usdt_trc20 = get_latest_usdt_trc20()
    latest_usdt_erc20 = get_latest_usdt_erc20()
    latest_btc = get_latest_btc()

    # Create a list of dictionaries containing the address information
    latest_addresses = [
        {'coin_name': 'BITCOIN', 'wallet_address': latest_btc.wallet_address, 'qr_code': latest_btc.qr_code, 'coin_icon': 'ph-lightning-light'},
        {'coin_name': 'USDT TRC20', 'wallet_address': latest_usdt_erc20.wallet_address, 'qr_code': latest_usdt_erc20.qr_code, 'coin_icon': 'ph-fire-simple-light'},
        {'coin_name': 'USDT ERC20', 'wallet_address': latest_usdt_trc20.wallet_address, 'qr_code': latest_usdt_trc20.qr_code, 'coin_icon': 'ph-file-light'},
    ]

    user = request.user
    # Fetch account balances and last four digits for each account type
    usdt_trc20_details = get_account_details(user, 'USDT_TRC20')
    usdt_erc20_details = get_account_details(user, 'USDT_ERC20')
    btc_details = get_account_details(user, 'BTC')

    # Create context
    context = {
        'usdt_trc20_balance': usdt_trc20_details['usdt_trc20_balance'],
        'usdt_erc20_balance': usdt_erc20_details['usdt_erc20_balance'],
        'btc_balance': btc_details['btc_balance'],
        'usdt_trc20_last_digits': usdt_trc20_details['usdt_trc20_last_digits'],
        'usdt_erc20_last_digits': usdt_erc20_details['usdt_erc20_last_digits'],
        'btc_last_digits': btc_details['btc_last_digits'],
        'latest_addresses': latest_addresses,
    }

    # Provide information/note on how to use the services
    return render(request, 'dashboard_T/transfer.html', context)

