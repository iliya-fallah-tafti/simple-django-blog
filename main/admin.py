from django.contrib import admin
from main.models import *
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created')
    list_filter = ('name', 'email')
    search_fields = ('name', 'message', 'subject')