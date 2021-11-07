from django.contrib import admin
from django.urls import path,include
from .views import Index,signup,Login,logout,cart,checkout,orders
from store.middlewares.auth import auth_middleware

urlpatterns = [
    
    path('',Index.as_view(),name='homepage'),
    path('signup/',signup,name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',logout,name='logout'),
    path('cart/',cart,name='cart'),
    path('checkout/',auth_middleware(checkout),name='checkout'),
    path('orders/',auth_middleware(orders),name='orders'),
]