from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from orders.models import Order

from .forms import ProfileForm, RegisterForm
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)  # корзина в сессии при входе сохраняется
        next_url = request.GET.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(
            next_url, allowed_hosts={request.get_host()}
        ):
            return redirect(next_url)
        return redirect('accounts:profile')

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Данные сохранены.')
        return redirect('accounts:profile')

    orders = request.user.orders.all()
    return render(
        request, 'accounts/profile.html', {'form': form, 'orders': orders}
    )


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items'), pk=pk, user=request.user
    )
    return render(request, 'accounts/order_detail.html', {'order': order})
