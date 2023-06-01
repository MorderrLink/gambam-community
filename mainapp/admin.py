from django.contrib import admin
from .models import *

# Register your models here.



class OrderAdmin(admin.ModelAdmin):
    search_fields = ("transaction_id", "id")
    list_display = ["id", "transaction_id", "completed", "finished"]

class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("date_added", "id", "order__transaction_id", "order__id")
    list_display = ["order", "product"]

admin.site.register(Picture)
admin.site.register(Post)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)