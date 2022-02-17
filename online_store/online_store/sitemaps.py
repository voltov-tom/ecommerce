from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from store.models import Category, Product


def lastmod(obj):
    return obj.date_added


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['frontpage', 'about', 'contact']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all()


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
