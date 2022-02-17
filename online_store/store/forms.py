from django.forms import ModelForm, ImageField

from store.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('title',)
        widgets = {
            'name': ImageField(),
        }
