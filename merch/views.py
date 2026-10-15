from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.filter(is_active=True)
    kind = request.GET.get('kind')
    if kind in Product.Kind.values:
        products = products.filter(kind=kind)
    return render(
        request,
        'merch/list.html',
        {
            'products': products,
            'kinds': Product.Kind.choices,
            'current_kind': kind,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'merch/detail.html', {'product': product})
