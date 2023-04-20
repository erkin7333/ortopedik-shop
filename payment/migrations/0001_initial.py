# Generated by Django 4.1.7 on 2023-04-20 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_payed', models.BooleanField(blank=True, default=False, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('amount_for_payme', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('number_of_people', models.IntegerField(blank=True, default=1, null=True)),
                ('place_id', models.IntegerField(blank=True, null=True)),
                ('place_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('customer_full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_passport', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_phone_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
