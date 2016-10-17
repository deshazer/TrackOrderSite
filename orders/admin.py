from django.contrib import admin

# Register your models here.

from .models import Product, LineItem, Order, Event, Person, Manufacturer


class PersonAdmin(admin.ModelAdmin):
    fields = [
        'first_name',
        'last_name',
        'phone',
        'address',
        'employer'
    ]


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    fields = [
        'isOpen',
        'order_date',
        'numPO'
    ]
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class ManufacturerAdmin(admin.ModelAdmin):
    pass


class LineItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(LineItem, LineItemAdmin)

