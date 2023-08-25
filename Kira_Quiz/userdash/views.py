
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

def userdash_home(request):
    # Your logic for the default userdash page
    return render(request, 'userdash/userdash_home.html')


def user_profile(request): 
    
    return render(request, 'userdash/userprofile.html')



def real_account(request):
	return render(request, 'userdash/real_account.html')

def demo_account(request):
	return render(request, 'userdash/demo_account.html')

def quizzes(request):
	return render(request, 'userdash/quizzes.html')





