# Generated by Django 5.0.6 on 2024-07-14 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_book_description_alter_book_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='avability',
            field=models.BooleanField(default=True),
        ),
    ]
