from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import AdminDashboard, AdminDeposit, AdminWithdraw, AdminProfile,AdminAccount
from raccount.models import UserProfile, Deposit, Withdraw, Account, Pay_quizz, Paid_quizz, Profite
from django.db.models import Sum, OuterRef, Subquery
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
  # Redirects non-staff members to the admin login page
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Replace with your admin dashboard URL
        else:
            error_message = "Invalid credentials or not an admin user."
            return render(request, 'admindash/admin_login.html', {'error_message': error_message})

    return render(request, 'admindash/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')  # Replace with your admin login URL



def admin_dashboard(request):
    admin_stats = AdminDashboard.objects.first()
    new_users_count = UserProfile.objects.filter(user__date_joined__gte=timezone.now() - timedelta(days=30)).count()
    user_deposits = Deposit.objects.aggregate(Sum('amount'))['amount__sum']
    user_withdraws = Withdraw.objects.aggregate(Sum('amount'))['amount__sum']
    user_pay_quizzes = Pay_quizz.objects.aggregate(Sum('amount'))['amount__sum']
    user_paid_quizzes = Paid_quizz.objects.aggregate(Sum('amount'))['amount__sum']
    active_users_count = Deposit.objects.values('user').distinct().count()

    # Calculate the total balance of all users (accounting for deposits and negative withdrawals)
    all_users_balance = user_deposits - user_withdraws


    #calculate Profite
    profite_from_users = user_pay_quizzes - user_paid_quizzes


    
    if admin_stats:
        admin_stats.new_users_count = new_users_count
        admin_stats.user_deposits = user_deposits if user_deposits else 0
        admin_stats.user_withdraws = user_withdraws if user_withdraws else 0
        admin_stats.user_pay_quizzes = user_pay_quizzes if user_pay_quizzes else 0
        admin_stats.user_paid_quizzes = user_paid_quizzes if user_paid_quizzes else 0
        admin_stats.active_users_count = active_users_count
        admin_stats.save()
    else:
        AdminDashboard.objects.create(
            new_users_count=new_users_count,
            user_deposits=user_deposits if user_deposits else 0,
            user_withdraws=user_withdraws if user_withdraws else 0,
            user_pay_quizzes = user_pay_quizzes if user_pay_quizzes else 0,
            user_paid_quizzes = user_paid_quizzes if user_paid_quizzes else 0,
            active_users_count=active_users_count
        )

    return render(request, 'admindash/admin_dash.html', {
        'admin_stats': admin_stats,
        'all_users_balance': all_users_balance,
        'profite_from_users':profite_from_users,

    })

  
def adminback(request):
    
    adminprofile = AdminProfile.objects.filter(adminuser=request.user.is_superuser).first()
    admindeposits = AdminDeposit.objects.filter(adminuser=request.user.is_superuser)
    adminwithdraws = AdminWithdraw.objects.filter(adminuser=request.user.is_superuser)
    try:
        adaccount = AdminAccount.objects.get(adminuser=request.user.is_superuser)
    except AdminAccount.DoesNotExist:
    # Handle the case where the AdminAccount doesn't exist for the superuser
    # You might want to create the account or handle the situation in another way
        adaccount = None
  

    #adaccount = AdminAccount.objects.get(adminuser=request.user.is_superuser)

    user_deposits_sum = Deposit.objects.filter(user=request.user).aggregate(Sum('amount'))
    user_deposits = user_deposits_sum['amount__sum'] or Decimal(0)

    user_withdraws_sum = Withdraw.objects.filter(user=request.user).aggregate(Sum('amount'))
    user_withdraws = user_withdraws_sum['amount__sum'] or Decimal(0)

    all_users_balance = user_deposits - user_withdraws

    if request.method == 'POST':
        if 'admindeposit_amount' in request.POST:
            admindeposit_amount = request.POST.get('admindeposit_amount')
            if admindeposit_amount:
                admindeposit_amount = int(admindeposit_amount)
                if admindeposit_amount > 0:
                    # Update the admin's balance after deposit
                    
                    if adaccount is not None:
    # Update the admin's balance after deposit
                        adaccount.balance += admindeposit_amount
                        adaccount.save()

                    # Record the admin deposit in the AdminDeposit model
                    AdminDeposit.objects.create(adminuser=request.user, amount=admindeposit_amount)

                    return redirect('adminback')

        
        elif 'adminwithdraw_amount' in request.POST:
            adminwithdraw_amount = request.POST.get('adminwithdraw_amount')
            if adminwithdraw_amount:
                adminwithdraw_amount = int(adminwithdraw_amount)

                if adaccount is not None:
                    if adminwithdraw_amount > 0 and adminwithdraw_amount <= adaccount.balance:
                # Update the admin's balance after withdrawal
                       adaccount.balance -= adminwithdraw_amount
                       adaccount.save()

                # Record the admin withdrawal in the AdminWithdraw model
                       AdminWithdraw.objects.create(adminuser=request.user, amount=adminwithdraw_amount)

                       return redirect('adminback')
                    else:
                # Handle the case where withdrawal amount is invalid
                        pass
                else:
            # Handle the case where adaccount is None
                    pass
 
              
    admindeposits_sum = AdminDeposit.objects.filter(adminuser=request.user).aggregate(Sum('amount'))
    adminwithdraws_sum = AdminWithdraw.objects.filter(adminuser=request.user).aggregate(Sum('amount'))

    admindeposits = admindeposits_sum['amount__sum'] or Decimal(0)
    adminwithdraws = adminwithdraws_sum['amount__sum'] or Decimal(0)

    QuizBalance = float(all_users_balance + (admindeposits - adminwithdraws))
    AdminBalance = float(admindeposits - adminwithdraws)

    
    return render(request, 'admindash/admin_backup.html', {
        'admindeposits': admindeposits,
        'adminwithdraws': adminwithdraws,
        'AdminBalance': QuizBalance,
        'adminprofile': adminprofile,
        'AdminBalance':AdminBalance,
    })





