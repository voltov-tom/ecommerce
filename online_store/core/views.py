from django.shortcuts import render

from store.models import Product, Category
from cart.cart import Cart

recently_viewed_products = Product.objects.all().order_by('-last_visit')[:4]


def frontpage(request):
    products = Product.objects.filter(is_futured=True, parent=None)
    parent_categories = Category.objects.filter(parent=None)
    popular_products = Product.objects.all().order_by('-num_visits')[:4]

    context = {
        'products': products,
        'parent_categories': parent_categories,
        'cart': Cart(request),
        'popular_products': popular_products,
        'recently_viewed_products': recently_viewed_products
    }
    return render(request, 'frontpage.html', context)


def contact(request):
    return render(request, 'contact.html', {'recently_viewed_products': recently_viewed_products})


def about(request):
    return render(request, 'about.html', {'recently_viewed_products': recently_viewed_products})
