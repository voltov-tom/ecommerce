import datetime

from urllib import request
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_name(obj):
    return f'{obj.first_name} {obj.last_name}'


order_name.short_description = 'Name'


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))


order_name.short_description = 'PDF Title'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def admin_order_shipped(ModelAdmin, request, queryset):
    for order in queryset:
        order.shipped_date = datetime.datetime.now()
        order.status = order.SHIPPED
        order.save()

        html = render_to_string('order_sent.html', {'order': order})
        send_mail(
            'Order sent',
            'Your order has been sent!',
            'noreply@online_store.com',
            ['mail@online_store.com', order.email],
            html_message=html
        )
    return


admin_order_shipped.short_description = 'Set shipped'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', order_name, 'status', 'created_at', order_pdf]
    list_filter = ['created_at', 'status']
    search_fields = ['first_name', 'address']
    inlines = [OrderItemInline]
    actions = [admin_order_shipped]


admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)
