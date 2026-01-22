from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__name')

admin.site.register(Order, OrderAdmin)
