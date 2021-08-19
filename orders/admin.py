from django.contrib import admin
from .models import Order, Customer, Scaffolding, Deliver


admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Scaffolding)
admin.site.register(Deliver)
