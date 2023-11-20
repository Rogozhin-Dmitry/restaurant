from json import loads

from django.forms import Form
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from core.models import Dish, OrderDish, Order, Table


class Menu(TemplateView):
    TEMPLATE = "waiter/menu.html"

    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.published_dishes_with_category_name_and_tag_name()
        context = {
            "dishes": dishes,
        }
        response = render(request, self.TEMPLATE, context)
        response.delete_cookie('dishes', path='waiter')
        return response


class Sorry(TemplateView):
    def get(self, request, order_pk, *args, **kwargs):
        order = Order.objects.actual_order_by_id(order_pk)
        if order:
            new_dish = OrderDish()
            new_dish.dish = Dish.objects.get_sorry_dish()
            new_dish.order = order
            new_dish.save()

        return redirect('waiter:orders')


class Pay(TemplateView):
    TEMPLATE = "waiter/pay.html"

    def get(self, request, order_pk, *args, **kwargs):
        order = Order.objects.actual_order_by_id(order_pk)
        if order:
            order.is_payed = True
            order.save()
            sum_to_pay = Order.objects.sum_to_pay_by_order_id(order_pk)
            if sum_to_pay:
                context = {
                    "sum": sum_to_pay
                }
                return render(request, self.TEMPLATE, context)
        return redirect('waiter:orders')


class Done(TemplateView):
    def get(self, request, order_pk, *args, **kwargs):
        order = Order.objects.actual_order_by_id(order_pk)
        if order:
            order.is_done = True
            order.save()

        return redirect('waiter:orders')


class Orders(TemplateView):
    TEMPLATE = "waiter/orders.html"

    def get(self, request, *args, **kwargs):
        orders_not_done, orders_done, orders_payed = Order.objects.actual_orders_this_dishes_done_nd_not_done()
        context = {
            "orders_not_done": orders_not_done,
            "orders_done": orders_done,
            "orders_payed": orders_payed,
        }
        return render(request, self.TEMPLATE, context)


class Cart(TemplateView):
    TEMPLATE = "waiter/cart.html"

    def get(self, request, *args, **kwargs):
        dishes = request.COOKIES.get("dishes", '{}')
        dishes_dict = loads(dishes)
        dishes_ids = dishes_dict.keys()
        dishes = Dish.objects.published_dishes_name_by_ids(dishes_ids)
        for dish in dishes:
            dish.count = dishes_dict[str(dish.pk)]
        context = {
            "dishes": dishes,
            "form": Form(),
            "tables": Table.objects.un_private_tables(),
        }
        return render(request, self.TEMPLATE, context)

    def post(self, request):
        if request.method == 'POST':
            dishes_count = request.COOKIES.get("dishes", '{}')
            dishes_count = loads(dishes_count)

            table_id = dict(request.POST.items())["places"]

            dishes_ids = dishes_count.keys()

            dishes = Dish.objects.published_dishes_name_by_ids(dishes_ids)
            order = Order()
            order.table = Table.objects.un_private_table_by_id(table_id)
            if dishes:
                order.save()
            for dish in dishes:
                new_dish = OrderDish()
                new_dish.dish = dish
                new_dish.order = order
                new_dish.quantity = dishes_count.get(str(dish.pk), 1)
                new_dish.save()
            return redirect('waiter:menu')
        return redirect('waiter:cart')
