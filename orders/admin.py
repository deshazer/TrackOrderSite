from django.contrib import admin
from django.forms import Textarea, TextInput
from django.db import models

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


class PersonInline(admin.TabularInline):
    model = Person
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})}}
    pass


class ManufacturerAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40})}}
    inlines = [ProductInline, PersonInline]


class LineItemAdmin(admin.ModelAdmin):
    fields = [
        'order',
        'product',
        'qty'
    ]



class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 0


class EventInline(admin.TabularInline):
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})}}
    model = Event
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    fields = [
        'isOpen',
        'order_date',
        'numPO'
    ]
    search_fields = ['numPO']
    inlines = [LineItemInline, EventInline]
    list_display = ('numPO', 'order_date', 'isOpen' )
    list_filter = ['order_date']



#admin.site.register(Product, ProductAdmin)
#admin.site.register(Person, PersonAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
#admin.site.register(Event, EventAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(LineItem, LineItemAdmin)

