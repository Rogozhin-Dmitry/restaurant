from django.urls import path

from waiter.views import Menu, Cart, Orders, Sorry, Pay, Done

app_name = 'waiter'

urlpatterns = [
    path("", Menu.as_view(), name='menu'),
    path("cart/", Cart.as_view(), name='cart'),
    path("orders/", Orders.as_view(), name='orders'),
    path("sorry/<int:order_pk>/", Sorry.as_view(), name='sorry'),
    path("pay/<int:order_pk>", Pay.as_view(), name='pay'),
    path("done/<int:order_pk>", Done.as_view(), name='done'),
]
