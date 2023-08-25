from django.contrib import admin
from .models import UserProfile, Deposit, Withdraw, Account, Pay_quizz, Paid_quizz, Profite

admin.site.register(UserProfile)
admin.site.register(Deposit)
admin.site.register(Withdraw)
admin.site.register(Account)
admin.site.register(Pay_quizz)
admin.site.register(Paid_quizz)
admin.site.register(Profite)

