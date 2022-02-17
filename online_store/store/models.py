from typing import Any

import os

from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models

from online_store.settings import MEDIA_ROOT


def make_thumbnail(image, size=(300, 200)):
    img = Image.open(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail(size)
    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)
    thumbnail = File(thumb_io, name=image.name)

    return thumbnail


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)
    is_futured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        if self.parent:
            return f'{self.parent.title}:{self.title}'
        else:
            return f'{self.title}'

    def get_absolute_url(self):
        return self.slug


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)

    image = models.ImageField(blank=True, null=True, default='no_photo.jpeg')
    thumbnail = models.ImageField(blank=True, null=True, default='no_photo.jpeg')

    is_futured = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    num_available = models.IntegerField(default=1)
    num_visits: Any = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-date_added',)

    def get_absolute_url(self):
        return self.slug

    # def save(self, *args, **kwargs):
    #     try:
    #         self.thumbnail = make_thumbnail(self.image)
    #     except ValueError:
    #         self.image.name = 'no_photo.jpeg'
    #         self.image.__path__ = MEDIA_ROOT / self.image.name
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category}: {self.title}'

    def get_thumbnail(self):
        print('get_thumbnail')
        if self.thumbnail and Path(self.thumbnail.__path__).is_file():
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = make_thumbnail(self.image)
                self.save()
            else:
                return MEDIA_ROOT / 'no_photo.jpeg'

    def get_rating(self):
        try:
            rating = sum(int(review['stars']) for review in self.reviews.values()) / self.reviews.count()
            return rating
        except ZeroDivisionError:
            return 0

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super().save(*args, **kwargs)
    #
    #         if not self.image.path == os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg'):
    #             poss_path = self.image.path
    #
    #             try:
    #                 super().save(*args, **kwargs)
    #                 new_image_name = os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg')
    #                 os.rename(self.image.path, new_image_name)
    #                 self.image.name = f'{self.slug}.jpeg'
    #                 self.image.__path__ = new_image_name
    #
    #             except FileExistsError:
    #                 os.remove(poss_path)
    #                 self.image.name = f'{self.slug}.jpeg'
    #                 self.image.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg')
    #                 super().save(*args, **kwargs)
    #
    #         if os.path.exists(os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')):
    #             self.thumbnail.name = f'{self.slug}-small.jpeg'
    #             self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #         else:
    #             try:
    #                 self.thumbnail = make_thumbnail(self.image)
    #                 super().save(*args, **kwargs)
    #                 new_thumbnail_path = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #                 os.rename(self.thumbnail.path, new_thumbnail_path)
    #                 self.thumbnail.name = f'{self.slug}-small.jpeg'
    #                 self.thumbnail.__path__ = new_thumbnail_path
    #
    #             except FileExistsError:
    #                 os.remove(self.thumbnail.path)
    #                 self.thumbnail.name = f'{self.slug}.jpeg'
    #                 self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #
    #     else:
    #         self.image.name = 'no_photo.jpeg'
    #         self.thumbnail.name = 'no_photo.jpeg'
    #         self.image.__path__ = os.path.join(MEDIA_ROOT, 'no_photo.jpeg')
    #         self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, 'no_photo.jpeg')
    #
    #     return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, default='no_photo.jpeg')
    thumbnail = models.ImageField(blank=True, null=True, default='no_photo.jpeg')

    def save(self, *args, **kwargs):
        self.thumbnail = make_thumbnail(self.image)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.image.name

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         super().save(*args, **kwargs)
    #
    #         if not self.image.path == os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg'):
    #             poss_path = self.image.path
    #
    #             try:
    #                 super().save(*args, **kwargs)
    #                 new_image_name = os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg')
    #                 os.rename(self.image.path, new_image_name)
    #                 self.image.name = f'{self.slug}.jpeg'
    #                 self.image.__path__ = new_image_name
    #
    #             except FileExistsError:
    #                 os.remove(poss_path)
    #                 self.image.name = f'{self.slug}.jpeg'
    #                 self.image.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}.jpeg')
    #                 super().save(*args, **kwargs)
    #
    #         if os.path.exists(os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')):
    #             self.thumbnail.name = f'{self.slug}-small.jpeg'
    #             self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #         else:
    #             try:
    #                 self.thumbnail = make_thumbnail(self.image)
    #                 super().save(*args, **kwargs)
    #                 new_thumbnail_path = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #                 os.rename(self.thumbnail.path, new_thumbnail_path)
    #                 self.thumbnail.name = f'{self.slug}-small.jpeg'
    #                 self.thumbnail.__path__ = new_thumbnail_path
    #
    #             except FileExistsError:
    #                 os.remove(self.thumbnail.path)
    #                 self.thumbnail.name = f'{self.slug}.jpeg'
    #                 self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, f'{self.slug}-small.jpeg')
    #
    #     else:
    #         self.image.name = 'no_photo.jpeg'
    #         self.thumbnail.name = 'no_photo.jpeg'
    #         self.image.__path__ = os.path.join(MEDIA_ROOT, 'no_photo.jpeg')
    #         self.thumbnail.__path__ = os.path.join(MEDIA_ROOT, 'no_photo.jpeg')
    #
    #     return super().save(*args, **kwargs)


class ProductsReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
