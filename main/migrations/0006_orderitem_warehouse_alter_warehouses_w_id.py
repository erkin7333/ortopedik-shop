# Generated by Django 4.1.7 on 2023-03-07 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_warehouses_products_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='warehouse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='warehouses',
            name='w_id',
            field=models.IntegerField(verbose_name='Sklad raqami'),
        ),
    ]
