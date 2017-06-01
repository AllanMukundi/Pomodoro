from .models import Item
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def shop(request):
    """
    Function based view for accessing the shop
    """
    items = Item.objects.all().order_by('-price')
    return render(request, 'shop.html', {'items': items})

