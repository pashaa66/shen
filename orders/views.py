from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from .shipping import calculate_shipping


def cart_detail(request):
    cart = Cart(request)
    return render(
        request, 'orders/cart.html', {'cart': cart, 'lines': cart.lines()}
    )


@require_POST
def cart_update(request, item_id):
    try:
        qty = int(request.POST.get('qty', 1))
    except ValueError:
        qty = 1
    Cart(request).set_qty(item_id, qty)
    return redirect('orders:cart')


@require_POST
def cart_remove(request, item_id):
    Cart(request).remove(item_id)
    return redirect('orders:cart')


@login_required
def checkout(request):
    cart = Cart(request)
    lines = cart.lines()
    if not lines:
        return redirect('orders:cart')

    items_total = cart.total_price
    shipping = calculate_shipping(items_total)

    initial = {}
    if request.user.is_authenticated:
        initial['email'] = request.user.email
        profile = getattr(request.user, 'profile', None)
        if profile:
            initial.update(
                full_name=profile.full_name,
                phone=profile.phone,
                address=profile.address,
                nickname=profile.nickname,
            )
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = (
                request.user if request.user.is_authenticated else None
            )
            order.items_total = items_total
            order.shipping_price = shipping
            order.total = items_total + shipping
            order.save()
            for line in lines:
                OrderItem.objects.create(
                    order=order,
                    product=line['product'],
                    title=f'{line["product"].title} {line["product"].size}'.strip(),
                    variant=line['variant'],
                    text=line['text'],
                    custom_image=line['image'],
                    unit_price=line['unit_price'],
                    quantity=line['qty'],
                )
        cart.clear()
        return redirect('orders:pay', token=order.token)

    return render(
        request,
        'orders/checkout.html',
        {
            'form': form,
            'lines': lines,
            'items_total': items_total,
            'shipping': shipping,
            'total': items_total + shipping,
        },
    )


def payment_mock(request, token):
    """Имитация оплаты. Позже заменяется на создание платежа в ЮKassa и обработку её уведомления."""
    order = get_object_or_404(Order, token=token)
    if order.status == Order.Status.PAID:
        return redirect('orders:done', token=order.token)
    if order.status == Order.Status.CANCELLED:
        return redirect('merch:list')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'pay':
            order.mark_paid()
            return redirect('orders:done', token=order.token)
        if action == 'cancel':
            with transaction.atomic():
                Cart(request).restore_from_order(order)
                order.delete()  # файлы картинок остаются на диске, они теперь в корзине
            messages.info(
                request, 'Оплата отменена. Товары вернулись в корзину.'
            )
            return redirect('orders:cart')

    return render(request, 'orders/payment_mock.html', {'order': order})


def order_done(request, token):
    order = get_object_or_404(Order, token=token)
    if order.status != Order.Status.PAID:
        return redirect('orders:pay', token=order.token)
    return render(request, 'orders/done.html', {'order': order})
