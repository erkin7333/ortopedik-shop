# Generated by Django 4.1.7 on 2023-04-20 08:16

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='blog/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=1000, verbose_name='Joylashuv')),
                ('address', models.CharField(max_length=400, verbose_name='Manzil')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon raqam')),
                ('phone1', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefon raqam')),
                ('email', models.CharField(max_length=100, verbose_name='Elektron manzil')),
            ],
            options={
                'verbose_name': 'Contact',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Requestforhelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='F.I.O')),
                ('phone', models.CharField(max_length=20, verbose_name='Telefon raqam')),
                ('email', models.CharField(max_length=100, verbose_name='Elektron manzil')),
                ('company', models.CharField(max_length=255, verbose_name='Kompaniya nomi')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Requestforhelp',
            },
        ),
        migrations.CreateModel(
            name='ContactTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=25, verbose_name='Sayt nomi')),
                ('subject', models.CharField(max_length=255, verbose_name='Qisqacha malumot')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contact.contact')),
            ],
            options={
                'verbose_name': 'Contact Translation',
                'db_table': 'contact_contact_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlogTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('subject', models.CharField(max_length=500, verbose_name='Subject')),
                ('description', models.TextField()),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='contact.blog')),
            ],
            options={
                'verbose_name': 'Blog Translation',
                'db_table': 'contact_blog_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
