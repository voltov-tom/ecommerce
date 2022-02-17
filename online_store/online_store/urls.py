from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views

from core.views import frontpage, contact, about
from store.views import product_detail, category_detail, search
from cart.views import cart_detail, success
from cart.webhook import webhook
from order.views import admin_order_pdf
from userprofile.views import signup, my_account

from newsletter.api import api_add_subscriber
from store.api import api_add_to_cart, api_remove_from_cart, create_checkout_session, api_remove_all_from_cart, \
    validate_payment
from coupon.api import api_can_use

from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {'static': StaticViewSitemap, 'product': ProductSitemap, 'category': CategorySitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('contact/', contact, name='contact'),
    path('hooks/', webhook, name='webhook'),
    path('about/', about, name='about'),
    path('search/', search, name='search'),
    path('search/', search, name='search'),
    path('cart/', cart_detail, name='cart'),
    path('cart/success/', success, name='success'),
    path('admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),

    path('signup/', signup, name='signup'),
    path('myaccount/', my_account, name='myaccount'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('api/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('api/validate-payment/', validate_payment, name='validate_payment'),
    path('api/add-to-cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove-from-cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/remove-all-from-cart/', api_remove_all_from_cart, name='api_remove_all_from_cart'),
    path('api/can-use/', api_can_use, name='api_can_use'),
    path('api/add-subscriber/', api_add_subscriber, name='api_add_subscriber'),
    # path('api/checkout/', api_checkout, name='api_checkout'),

    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
