from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    prod_description = models.CharField(max_length=255)
    sku = models.IntegerField()
    unit_price = models.FloatField(default=0.0)
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sku',)


class Order(models.Model):
    isOpen = models.BooleanField(default=True)  # Mark order as Open/Closed
    order_date = models.DateTimeField('date submitted')
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
        return "PO: %08d" % int(self.numPO)

    class Meta:
        ordering = ('order_date',)


class LineItem(models.Model):
    qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return "Item: %s x%d on PO: %d" % \
            (self.product.name, int(self.qty), int(self.order.numPO))


class Event(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event_date = models.DateTimeField()
    event_description = models.TextField(max_length=255)

    def __str__(self):
        return self.event_description


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
