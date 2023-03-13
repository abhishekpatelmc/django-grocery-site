from django.http import HttpResponse

from .forms import OrderItemForm
from .models import Type, Item
from django.shortcuts import render, get_object_or_404
from django.views.generic import View


def index(request):
    # return render(request, 'myapp/index.html', {'type_list': type_list})
    #     item_list = Item.objects.all().order_by('-price')[:10]
    # return render(request, 'myapp1/index.html', {'item_list': item_list})
    type_list = Type.objects.all().order_by('id')[:7]
    return render(request, 'myapp1/index.html', {'type_list': type_list})
    # response = HttpResponse()
    # heading1 = '<p>' + 'Different Types: ' + '</p>'
    # response.write(heading1)
    # for item in type_list:
    #     para = '<p>' + str(item.name) + ': ' '</p>'
    #     response.write(para)
    # return response


# Yes, I am passing type_list as an extra context variable to the templates


def about(request):
    # No, I am not passing any additional context variable to the templates
    return render(request, 'myapp1/about.html')


def detail(request, type_no):
    detaillist = get_object_or_404(Type, id=type_no)
    # Yes, I am passing type as an extra context variable to the templates
    return render(request, 'myapp1/detail.html', {'type': detaillist})


def items(request):
    itemlist = Item.objects.all().order_by('id')[:20]
    return render(request, 'myapp1/items.html', {'itemlist': itemlist})


def placeorder(request):
    msg = ""
    itemlist = Item.objects.all()
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.ordered_item <= int(order.item.stock):
                order.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'myapp1/order_response.html', {'msg': msg})
    else:
        form = OrderItemForm()
    return render(request, 'myapp1/placeorder.html', {'form': form, 'msg': msg, 'itemlist': itemlist})


# def placeorder(request):
#     itemlist = Item.objects.all()
#     return render(request, 'myapp1/placeorder.html', {'itemlist':itemlist})


# def about(request,year,month):
#     month_name = datetime.strftime(datetime(2000, month, 1), '%B')
#     response = HttpResponse()
#     response.write(f'<p>This is an Online Grocery Store - {month_name} {year}</p>')
#     return response
#
# def detail(request, type_no):
#     item_list = get_list_or_404(Item, type=type_no)
#      return render(request, 'myapp1/detail.html', {'type': type})

# FBV(function -based - view)
# Simple to write and understand.
# Good for basic logic.
def type_list(request):
    types = Type.objects.all()
    response = HttpResponse()
    for typ in types:
        response.write('<p>' + typ.name + '</p>')
    return response


# CBV(class-based-view)
# Can be inherited
# Reusable
# can handle complex logic
class TypeListView(View):
    def get(self, request):
        types = Type.objects.all()
        response = HttpResponse()
        for typ in types:
            response.write('<p>' + typ.name + '</p>')
        return response

