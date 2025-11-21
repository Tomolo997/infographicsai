from django.contrib import admin

# Register your models here.
from .models import InfoGraph
# admin.py
from django.contrib import admin
from .models import InfoGraph

@admin.register(InfoGraph)
class InfoGraphAdmin(admin.ModelAdmin):
    list_display = ('title', 'uuid', 'account', 'created_at', 'updated_at')  # Shows these fields as columns
    readonly_fields = ('uuid',)  # Makes UUID read-only in the edit form
    search_fields = ('title', 'uuid')  # Allows searching by title or UUID
    list_filter = ('created_at', 'updated_at')  # Adds filters on the right side
