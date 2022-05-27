from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, Address, UserProfile


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(UserProfile)
