from django.contrib import admin
from django.urls import path
from . import views

app_name = 'myapp1'
urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('myorder/', views.myorder, name='myorder'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('detail/<str:type_no>/', views.detail, name='detail'),
    path('my_fbv/', views.my_fbv, name='my_fbv'),
    path('my_cbv/', views.MyCBV.as_view(), name='my_cbv'),
    path('items/', views.items, name='items'),
    path('items/<int:item_id>/', views.itemdetail, name='itemdetail'),
    path('placeorder/', views.placeorder, name='placeorder')


    # path('', include('myapp1.urls')),
]
