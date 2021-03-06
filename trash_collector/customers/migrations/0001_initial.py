# Generated by Django 3.1.8 on 2021-04-08 19:38

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
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(default=None, max_length=60)),
                ('street', models.CharField(default=None, max_length=50)),
                ('city', models.CharField(default=None, max_length=50)),
                ('zipcode', models.IntegerField(default=None)),
                ('account_status', models.BooleanField(default=True)),
                ('pickup_days', models.CharField(default=None, max_length=50)),
                ('specific_date', models.DateField(default=None)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
