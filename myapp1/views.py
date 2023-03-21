from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from myapp1.models import Type, Item, OrderItem
from myapp1.forms import OrderItemForm, InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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


def my_fbv(request):
    context = {
        'message': 'Hello, this is my Function-Based View (FBV)!'
    }
    return render(request, 'myapp1/my_template.html', context)


# Class-Based View (CBV)
class MyCBV(View):
    def get(self, request):
        context = {
            'message': 'Hello, this is my Class-Based View (CBV)!'
        }
        return render(request, 'myapp1/my_template.html', context)


def items(request):
    itemlist = Item.objects.all().order_by('id')[:20]
    return render(request, 'myapp1/items.html', {'itemlist': itemlist})


def placeorder(request):
    msg = ''
    itemlist = Item.objects.all()
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.no_of_order <= order.ordered_item.stock:
                order.save()
                order.ordered_item.stock -= order.no_of_order
                order.ordered_item.save()
                msg = 'Your order has been placed successfully.'
        else:
            msg = 'We do not have sufficient stock to fill your order.'
        return render(request, 'myapp1/order_response.html', {'msg': msg})
    else:
        form = OrderItemForm()
    return render(request, 'myapp1/placeorder.html', {'form': form, 'msg': msg, 'itemlist': itemlist})


def itemdetail(request, item_id):
    ordered_item = Item.objects.get(id=item_id)
    interested = ordered_item.interested
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']
            quantity = form.cleaned_data['quantity']
            comments = form.cleaned_data['comments']
            if interested:
                ordered_item.interested.__add__(request.user)
            else:
                ordered_item.interested.remove(request.user)
            ordered_item.save()
            # msg = 'Thanks for your interest!'
    else:
        form = InterestForm()
    return render(request, 'myapp1/itemdetail.html', {'item': ordered_item, 'interested': interested, 'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp1:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp1/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp1:user_login'))


def myorder(request):
    if request.user.is_active:
        orders = OrderItem.objects.filter(ordered_by=request.user)
        return render(request, 'myapp1/myorder.html', {'orders': orders})
    else:
        message = 'You are not a active client!'
        return render(request, 'myapp1/myorder.html', {'message': message})


# Good for basic logic.
def type_list(request):
    types = Type.objects.all()
    response = HttpResponse()
    for typ in types:
        response.write('<p>' + typ.name + '</p>')
    return response


class TypeListView(View):
    def get(self, request):
        types = Type.objects.all()
        response = HttpResponse()
        for typ in types:
            response.write('<p>' + typ.name + '</p>')
        return response
