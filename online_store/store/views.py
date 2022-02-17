import random
from datetime import datetime

from functools import reduce

from django.http import HttpResponseRedirect
from queryset_sequence import QuerySetSequence

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from store.models import Product, Category
from cart.cart import Cart

from .models import ProductsReview
from .serializers import product_images_serializer

recently_viewed_products = Product.objects.all().order_by('-last_visit')[:4]


def search(request):
    query = request.GET.get('query')
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 100000)
    sorting = request.GET.get('sorting', '-date_added')
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)).filter(
        price__gte=price_from).filter(
        price__lte=price_to
    )

    if instock:
        products = products.filter(num_available__gte=1)

    context = {
        'query': query,
        'instock': instock,
        'price_from': price_from,
        'price_to': price_to,
        'sorting': sorting,
        'products': products.order_by(sorting),
        'recently_viewed_products': recently_viewed_products
    }
    return render(request, 'search.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    product.num_visits += 1
    product.last_visit = datetime.now()
    product.save()

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 5)
        content = request.POST.get('content', '')

        review = ProductsReview.objects.create(user=request.user, product=product, stars=stars, content=content)

        return redirect('product_detail', category_slug=category_slug, slug=slug)

    if product.category.parent:
        related_products = []
        for child in product.category.parent.children.all():
            related_products.append(child.products.all().exclude(id=product.id))
        related_products = list(reduce(QuerySetSequence, related_products))
    else:
        related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))

    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)

    if product.parent:
        return redirect('product_detail', category_slug=category_slug, slug=product.parent.slug)

    image_string = product_images_serializer(product)

    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    context = {
        'product': product,
        'recently_viewed_products': recently_viewed_products,
        'imageString': image_string,
        'related_products': related_products
    }
    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(parent=None)
    context = {
        'recently_viewed_products': recently_viewed_products,
        'category': category,
        'products': products
    }
    return render(request, 'category_detail.html', context)
