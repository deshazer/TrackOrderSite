from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    prod_description = models.CharField(
        max_length=255, verbose_name='Product Description')
    sku = models.IntegerField(verbose_name='SKU')
    unit_price = models.FloatField(default=0.0)
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sku',)


class Order(models.Model):
    isOpen = models.BooleanField(
        default=True, verbose_name="Open?")  # Mark order as Open/Closed
    order_date = models.DateTimeField('Date Submitted')
    numPO = models.IntegerField(unique=True, default=0,
                                verbose_name="PO Number")   # Purchase Order number
    # Each order may contain multiple products w/ a quantity
    products = models.ManyToManyField(Product, through='LineItem')

    def get_status(self):
        if self.isOpen:
            return "open"
        else:
            return "closed"

    def __str__(self):
        return "PO: %d" % int(self.numPO)
    
    def save(self, *args, **kwargs):
        if self.id:
            new_order = False
            old = Order.objects.get(pk=self.id)
        else:
            new_order = True
        super(Order, self).save(*args, **kwargs)
        # If it's a new order, start an event history
        if new_order:
            e = Event.objects.create(
                order=self,
                event_date=self.order_date,
                event_description="Order submitted"
            )
        else:
            # If changing original order date, then
            # update the first event in the history
            # to match the new date
            if old.order_date != self.order_date:
                e = Event.objects.filter(
                    order__id=self.id).order_by('event_date')[0]
                e.event_date = self.order_date
                e.save()

    class Meta:
        ordering = ('order_date',)


class LineItem(models.Model):
    qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return "%dx -- %s -- PO: %d" % \
            (int(self.qty), self.product.name,  int(self.order.numPO))


class Event(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    event_description = models.TextField(max_length=255)

    def __str__(self):
        return "Order: %s -- %s -- Date: %s" % \
               (self.order.numPO, self.event_description, self.event_date)


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    address = models.TextField(max_length=255)
    phone = models.CharField(max_length=30)
    employer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name
