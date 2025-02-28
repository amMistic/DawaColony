# Generated by Django 5.1.5 on 2025-02-10 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.CharField(choices=[('MEDICINE', 'medicine'), ('HEALTHCARE', 'Healthcare'), ('WELLNESS', 'Wellness'), ('PERSONAL_CARE', 'Personal Care')], max_length=64)),
                ('description', models.CharField(max_length=256)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10000)),
                ('stock', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/create/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
