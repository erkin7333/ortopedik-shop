# Generated by Django 4.1.7 on 2023-04-20 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9, verbose_name="To'lov miqdori (so'mda)")),
                ('transaction_external_id', models.CharField(blank=True, default='', max_length=30)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(choices=[('click', 'Click')], default='click', max_length=10)),
                ('status', models.CharField(choices=[('new', 'New'), ('verified', 'Verified'), ('paid', 'Paid'), ('canceled', 'Canceled')], default='new', max_length=10)),
                ('comment', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ClickOrder',
                'verbose_name_plural': 'ClickOrders',
            },
        ),
    ]
