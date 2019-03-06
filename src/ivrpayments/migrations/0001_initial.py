# Generated by Django 2.1.7 on 2019-03-06 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pay_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_request', models.CharField(max_length=30)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('country', models.CharField(max_length=4)),
                ('currency', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('card_num', models.CharField(max_length=30)),
                ('cvc_num', models.CharField(max_length=3)),
                ('exp_month', models.CharField(max_length=2)),
                ('exp_year', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Pay_Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_response', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('currency', models.CharField(max_length=5)),
                ('country', models.CharField(max_length=4)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('recip_mail', models.EmailField(max_length=254)),
                ('description', models.CharField(max_length=50)),
                ('paid', models.BooleanField(default=False)),
                ('refunded', models.BooleanField(default=False)),
                ('card_last4', models.CharField(default=0, max_length=4)),
            ],
        ),
    ]
