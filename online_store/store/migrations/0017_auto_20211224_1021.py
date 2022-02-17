# Generated by Django 3.2.8 on 2021-12-24 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_category_is_futured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_visit',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]