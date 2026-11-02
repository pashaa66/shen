from django.shortcuts import get_object_or_404, redirect, render
from orders.cart import Cart

from .forms import AddToCartForm
from .models import Product, Variant
from .utils import save_custom_image


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

    if request.method == 'POST':
        form = AddToCartForm(request.POST, request.FILES, product=product)
        if form.is_valid():
            data = form.cleaned_data
            image_path = (
                save_custom_image(data['image'])
                if data['variant'] == Variant.CUSTOM
                else ''
            )
            Cart(request).add(
                product,
                variant=data['variant'],
                text=(data.get('text') or '').strip(),
                image_path=image_path,
                quantity=data['quantity'],
            )
            return redirect('orders:cart')
    else:
        form = AddToCartForm(product=product)

    return render(
        request, 'merch/detail.html', {'product': product, 'form': form}
    )
