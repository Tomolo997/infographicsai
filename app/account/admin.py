from django.contrib import admin

# Register your models here.
from account.models import Account, CreditPack, CustomUser

admin.site.register(Account)
admin.site.register(CustomUser)
admin.site.register(CreditPack)