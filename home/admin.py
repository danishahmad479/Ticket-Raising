from django.contrib import admin
from home.models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Roles)
admin.site.register(Department)
admin.site.register(Ticket)
admin.site.register(SendTicketTo)