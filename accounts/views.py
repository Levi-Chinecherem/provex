from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from payment.utils import get_latest_usdt_trc20, get_latest_usdt_erc20, get_latest_btc, get_account_details

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate passwords match
        if password1 != password2:
            # Handle password mismatch error
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})

        # You may add additional validation as needed

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Automatically log in the user after signup
        login(request, user)

        return redirect('dashboard')  # Redirect to the desired page after signup

    return render(request, 'accounts/signup.html')

@login_required
def profile(request):
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
    return render(request, 'accounts/profile.html', context)

def user_logout(request):
    logout(request)
    return redirect('home') 