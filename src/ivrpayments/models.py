from django.db import models

# Create your models here.

class Pay_Request(models.Model):
    id_request = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=4)
    currency = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    card_num = models.CharField(max_length=30)
    cvc_num = models.CharField(max_length=3)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=2)

class Pay_Response(models.Model):
    id_response = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    currency = models.CharField(max_length=5)
    country = models.CharField(max_length=4)
    amount = models.PositiveIntegerField(default=0)
    recip_mail = models.EmailField()
    description = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    card_last4 = models.CharField(max_length=4, default=0)


