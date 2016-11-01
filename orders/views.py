from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    order_list = Order.objects.order_by('-order_date')
    context = {'order_list': order_list}
    return render(request, 'orders/index.html', context)
