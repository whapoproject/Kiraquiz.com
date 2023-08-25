#views for realacc
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import UserProfile, Account, Deposit, Withdraw, Pay_quizz, Paid_quizz, Profite
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, OuterRef, Subquery
from .models import UserProfile, Account  # Assuming you have defined these models
# in views.py
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .forms import UserRegistrationForm
# views.py
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Account, Deposit, Withdraw, Pay_quizz, Paid_quizz, Profite
from .forms import UserRegistrationForm

"""def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('realacc/reg/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')

    return render(request, 'realacc/register.html', {'form': UserRegistrationForm()})
"""
from django.contrib.auth.models import User
from .models import UserProfile, Account

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile and Account for the newly registered user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            account, created = Account.objects.get_or_create(user=user)


            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('realacc/reg/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')

    else:
        form = UserRegistrationForm()  # Create an empty form

    return render(request, 'realacc/reg/register.html', {'form': form})



# in views.py
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user_login')
    else:
        return render(request, 'realacc/reg/account_activation_invalid.html')


# raccount/views.py
from django.shortcuts import render

def account_activation_sent(request):
    return render(request, 'realacc/reg/account_activation_sent.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userdash:userdash_home')
        else:
            # Add error handling for invalid login
            pass

    return render(request, 'realacc/user_login.html')

#dealing with reset password

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'realacc/res/password_reset_form.html'  # Your template
    form_class = PasswordResetForm  # Use the default form
    email_template_name = 'realacc/res/password_reset_email.html'  # Your email template
    subject_template_name = 'realacc/res/password_reset_subject.txt'  # Your email subject

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'realacc/res/password_reset_confirm.html'  # Your template

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'realacc/res/password_reset_done.html'  # Your template

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'realacc/res/password_reset_complete.html'  # Your template



@login_required
def real_account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)
    deposits = Deposit.objects.filter(user=request.user)
    withdraws = Withdraw.objects.filter(user=request.user)
    payquizzes = Pay_quizz.objects.filter(user=request.user)
    paidquizzes = Paid_quizz.objects.filter(user=request.user)
   


    if request.method == 'POST':
        if 'deposit_amount' in request.POST:
            deposit_amount = request.POST.get('deposit_amount')
            if deposit_amount:
                deposit_amount = int(deposit_amount)
                if deposit_amount > 0:
                    # Update the user's balance after deposit
                    account.balance += deposit_amount
                    account.save()

                    # Record the deposit in the Deposit model
                    Deposit.objects.create(user=request.user, amount=deposit_amount)

                    return redirect('real_account')

        elif 'withdraw_amount' in request.POST:
            withdraw_amount = request.POST.get('withdraw_amount')
            if withdraw_amount:
                withdraw_amount = int(withdraw_amount)
                if withdraw_amount > 0 and withdraw_amount <= account.balance:
                    # Update the user's balance after withdrawal
                    account.balance -= withdraw_amount
                    account.save()

                    # Record the withdrawal in the Withdraw model
                    Withdraw.objects.create(user=request.user, amount=withdraw_amount)

                    return redirect('real_account')

    return render(request, 'realacc/real_account.html', {
        'user_profile': user_profile,
        'account': account,
        'deposits': deposits,
        'withdraws': withdraws,
        'payquizzes':payquizzes,
        'paidquizzes':paidquizzes,
        #'profites':profites,
    })

def payment(request):
    account = Account.objects.get(user=request.user)
    # Calculate the total Profite for user is earning
    profites = Profite.objects.annotate(
        paidquizzes=Subquery(Paid_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            paidquizzes=Sum('amount')
        ).values('paidquizzes')),
        payquizzes=Subquery(Pay_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            payquizzes=Sum('amount')
        ).values('payquizzes')),
    ).annotate(
        net_profite=Sum('paidquizzes', distinct=True) - Sum('payquizzes', distinct=True)
    ).aggregate(Sum('net_profite'))['net_profite__sum']
    

   

    if request.method == 'POST':
        if 'payquizzes_amount' in request.POST:
            payquizzzes_amount = request.POST.get('payquizzes_amount')
            if payquizzzes_amount:
                payquizzzes_amount = int(payquizzzes_amount)
                if payquizzzes_amount > 0 and payquizzzes_amount <= account.balance:
                    # Update the user's balance after deposit
                    account.balance -= payquizzzes_amount
                    account.save()

                    # Record the deposit in the Deposit model
                    Pay_quizz.objects.create(user=request.user, amount=payquizzzes_amount)

                    return redirect('quiz_view')
    return render(request, 'realacc/pay/payment_0.html', {
        
        'profites':profites,
    })
    
    
def payment1(request):
    account = Account.objects.get(user=request.user)
    # Calculate the total Profite for user is earning
    profites = Profite.objects.annotate(
        paidquizzes=Subquery(Paid_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            paidquizzes=Sum('amount')
        ).values('paidquizzes')),
        payquizzes=Subquery(Pay_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            payquizzes=Sum('amount')
        ).values('payquizzes')),
    ).annotate(
        net_profite=Sum('paidquizzes', distinct=True) - Sum('payquizzes', distinct=True)
    ).aggregate(Sum('net_profite'))['net_profite__sum']
    

   

    if request.method == 'POST':
        if 'payquizzes_amount' in request.POST:
            payquizzzes_amount = request.POST.get('payquizzes_amount')
            if payquizzzes_amount:
                payquizzzes_amount = int(payquizzzes_amount)
                if payquizzzes_amount > 0 and payquizzzes_amount <= account.balance:
                    # Update the user's balance after deposit
                    account.balance -= payquizzzes_amount
                    account.save()

                    # Record the deposit in the Deposit model
                    Pay_quizz.objects.create(user=request.user, amount=payquizzzes_amount)

                    return redirect('quiz_view_01')
    return render(request, 'realacc/pay/payment_1.html', {
        
        'profites':profites,
    })

def payment2(request):
    account = Account.objects.get(user=request.user)
    # Calculate the total Profite for user is earning
    profites = Profite.objects.annotate(
        paidquizzes=Subquery(Paid_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            paidquizzes=Sum('amount')
        ).values('paidquizzes')),
        payquizzes=Subquery(Pay_quizz.objects.filter(user=OuterRef('user')).values('user').annotate(
            payquizzes=Sum('amount')
        ).values('payquizzes')),
    ).annotate(
        net_profite=Sum('paidquizzes', distinct=True) - Sum('payquizzes', distinct=True)
    ).aggregate(Sum('net_profite'))['net_profite__sum']
    

   

    if request.method == 'POST':
        if 'payquizzes_amount' in request.POST:
            payquizzzes_amount = request.POST.get('payquizzes_amount')
            if payquizzzes_amount:
                payquizzzes_amount = int(payquizzzes_amount)
                if payquizzzes_amount > 0 and payquizzzes_amount <= account.balance:
                    # Update the user's balance after deposit
                    account.balance -= payquizzzes_amount
                    account.save()

                    # Record the deposit in the Deposit model
                    Pay_quizz.objects.create(user=request.user, amount=payquizzzes_amount)

                    return redirect('quiz_view_02')
    return render(request, 'realacc/pay/payment_2.html', {
        
        'profites':profites,
    })
    

def paid_quizzes(request):
    paidquizzes = Paid_quizz.objects.filter(user=request.user)
    return render(request, 'realacc/trans/paid_quizzes.html', {'paidquizzes': paidquizzes})

def pay_quizzes(request):
    payquizzes = Pay_quizz.objects.filter(user=request.user)
    return render(request, 'realacc/trans/pay_quizzes.html', {'payquizzes': payquizzes})

def deposits(request):
    deposits = Deposit.objects.filter(user=request.user)
    return render(request, 'realacc/trans/deposits.html', {'deposits': deposits})

def withdraws(request):
    withdraws = Withdraw.objects.filter(user=request.user)
    return render(request, 'realacc/trans/withdraws.html', {'withdraws': withdraws})

