from django.contrib import admin
from .models import Demand, VerificationContent, Technology

# Register your models here.
admin.site.register(Demand)
admin.site.register(VerificationContent)
admin.site.register(Technology)