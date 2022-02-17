from django.contrib import admin

from .models import Category, Product, ProductImage, ProductsReview


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    exclude = ('thumbnail', 'clearable-file-input')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    exclude = ('thumbnail', 'clearable-file-input')


# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Category)
admin.site.register(ProductsReview)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductImage, ProductImageAdmin)
