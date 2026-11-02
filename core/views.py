from django.shortcuts import render

from merch.models import Product


def home(request):
    products = Product.objects.filter(is_active=True)[:4]
    return render(request, 'core/home.html', {'products': products})


def about(request):
    return render(request, 'core/about.html')


def not_found(request, exception):
    return render(request, '404.html', status=404)


def game(request):
    return render(request, 'core/game.html')
