# Generated by Django 4.2.4 on 2023-08-07 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0002_alter_item_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(max_length=510),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(max_length=510),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=510),
        ),
        migrations.AlterField(
            model_name='item',
            name='sku',
            field=models.CharField(max_length=510),
        ),
        migrations.AlterField(
            model_name='item',
            name='url',
            field=models.CharField(max_length=510),
        ),
    ]