from django.contrib import admin

# Register your models here.
from icons.models import SVGIcon, VectorIcon, Pattern, FlatIcon, OutlineIcon

admin.site.register(SVGIcon)
admin.site.register(VectorIcon)
admin.site.register(Pattern)
admin.site.register(FlatIcon)
admin.site.register(OutlineIcon)