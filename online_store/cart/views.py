from django.conf import settings
from django.shortcuts import render

from cart.cart import Cart

from .serializers import cart_serializer
from store.models import Product

recently_viewed_products = Product.objects.all().order_by('-last_visit')[:4]


def cart_detail(request):
    cart = Cart(request)
    json_cart_products = cart_serializer(cart)

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        zipcode = request.user.userprofile.zipcode
        phone = request.user.userprofile.phone
        place = request.user.userprofile.place
    else:
        first_name = last_name = email = address = zipcode = phone = place = ''

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address,
        'zipcode': zipcode,
        'phone': phone,
        'place': place,

        'cart': cart,
        'pub_key': settings.STRIPE_API_PUBLISHABLE_KEY,
        'pub_key_razorpay': settings.RAZORPAY_API_PUBLISHABLE_KEY,
        'pub_key_paypal': settings.PAYPAL_API_PUBLISHABLE_KEY,
        'json_cart_products': json_cart_products,
        'recently_viewed_products': recently_viewed_products
    }
    return render(request, 'cart.html', context)


def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'success.html')
