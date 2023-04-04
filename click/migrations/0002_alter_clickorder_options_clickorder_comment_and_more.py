# Generated by Django 4.1.7 on 2023-04-04 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('click', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clickorder',
            options={'verbose_name': 'ClickOrder', 'verbose_name_plural': 'ClickOrders'},
        ),
        migrations.AddField(
            model_name='clickorder',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='clickorder',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clickorder',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clickorder',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('verified', 'Verified'), ('paid', 'Paid'), ('canceled', 'Canceled')], default='new', max_length=10),
        ),
        migrations.AddField(
            model_name='clickorder',
            name='transaction_external_id',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='clickorder',
            name='transaction_type',
            field=models.CharField(choices=[('click', 'Click')], default='timezone.now', max_length=10),
            preserve_default=False,
        ),
    ]