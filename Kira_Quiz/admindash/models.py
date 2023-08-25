from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _


Group.objects.get_or_create(name='Admins')


class AdminDashboard(models.Model):
    new_users_count = models.IntegerField(default=0)
    active_users_count = models.IntegerField(default=0)
    user_deposits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_withdraws = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_all_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_pay_quizzes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_paid_quizzes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profite_from_users = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AdminProfile(models.Model):
    adminuser = models.OneToOneField(User, on_delete=models.CASCADE)
class AdminDeposit(models.Model):
    adminuser = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class AdminWithdraw(models.Model):
    adminuser = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
class AdminAccount(models.Model):
    adminuser = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

