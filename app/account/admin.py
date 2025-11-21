from django.contrib import admin

# Register your models here.
from account.models import Account, CustomUser, MagicLink, UserSubscription, SubscriptionTier, Suggestion


admin.site.register(Account)
admin.site.register(CustomUser)
admin.site.register(MagicLink)
admin.site.register(Suggestion)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionTier)