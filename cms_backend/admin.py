from django.contrib import admin
from .models import ticket
# Register your models here.


class ticketAdmin(admin.ModelAdmin):
    list_display = ['automatic_generated_ticket_number', 'name', 'phone_no', 'address', 'notes']



admin.site.register(ticket, ticketAdmin)
