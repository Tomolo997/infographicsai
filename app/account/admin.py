from django.contrib import admin

# Register your models here.
from account.models import Account, CreditPack, CreditPurchase, CustomUser

admin.site.register(Account)
admin.site.register(CustomUser)
admin.site.register(CreditPack)
admin.site.register(CreditPurchase)