from django.urls import path
from .views import MakePaymentView

urlpatterns = [
    path('charge/', MakePaymentView.as_view(), name='charge')
]