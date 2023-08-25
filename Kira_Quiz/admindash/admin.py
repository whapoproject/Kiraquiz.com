from django.contrib import admin
from .import models


admin.site.register(models.AdminDashboard)
admin.site.register(models.AdminDeposit)
admin.site.register(models.AdminWithdraw)
admin.site.register(models.AdminProfile)
admin.site.register(models.AdminAccount)

