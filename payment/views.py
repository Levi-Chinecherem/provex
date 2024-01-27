from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import get_account_details
from .models import Funds
from decimal import Decimal
from django.contrib import messages


@login_required
def funds_details(request):
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

    return render(request, 'chunks/side_balance.html', context)

def success_page(request):
    return render(request, 'message.html')

@login_required
def add_funds(request):
    user = request.user

    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        account_type = request.POST.get('account_type')

        # Handle the conversion to float gracefully
        try:
            amount = float(amount_str)
        except ValueError:
            # Handle the case where the conversion to float fails
            amount = 0.0  # Set a default value or handle the error appropriately
            messages.error(request, 'Invalid amount. Please enter a valid number.')

        else:
            # Create a new Funds object and save it
            fund = Funds.objects.create(user=user, account_type=account_type, amount=amount)

            # Add success message
            messages.success(request, f'Funds added successfully! Amount: {amount}')

            # Redirect to a success page
            return redirect('success_page')  # Replace 'success_page_name' with the actual name or URL of your success page

    # If the request method is not POST, render the add funds form
    return render(request, 'dashboard_T/transfer.html')  # Replace 'add_funds.html' with the actual template you want to use
