from django.contrib import admin
from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('base', 'target', 'rate', 'date',)
    list_filter = ('base', 'target', 'date', 'created',)
