# Generated by Django 4.1.7 on 2023-10-15 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='obrok.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]