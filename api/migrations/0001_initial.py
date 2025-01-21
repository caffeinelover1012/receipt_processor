# Generated by Django 5.1.5 on 2025-01-20 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retailer', models.CharField(max_length=255)),
                ('purchase_date', models.DateField()),
                ('purchase_time', models.TimeField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('items', models.ManyToManyField(to='api.item')),
            ],
        ),
    ]
