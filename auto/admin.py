from django.contrib import admin
from .models import Car, Manager, Rent, Renter, Review

admin.site.register(Car)
admin.site.register(Manager)
admin.site.register(Rent)
admin.site.register(Renter)
admin.site.register(Review)