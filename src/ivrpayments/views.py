import stripe

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
import logging
from .serializers import charge_create_serializer
from django.conf import settings

from ivrpayments.models import Pay_Request, Pay_Response

logger = logging.getLogger(__name__)


class MakePaymentView(CreateAPIView):
    queryset = Pay_Request.objects.all()
    serializer_class = charge_create_serializer



    def create(self, request, *args, **kwargs):
        """
        Creates the request and response model to the database while sending and receiving data from stripe
        :param request: It has the data from the rest form on the view
        :param args:
        :param kwargs:
        :return:
        """
        if request.method == 'POST':
            stripe.api_key = settings.STRIPE_SECRET_KEY

            pay_req = Pay_Request.objects.create(
                name=request.data['name'],
                email=request.data['email'],
                phone=request.data['phone'],
                card_num=request.data['card_num'],
                cvc_num=request.data['cvc_num'],
                exp_month=request.data['exp_month'],
                exp_year=request.data['exp_year'],
                description=request.data['description'],
                country=request.data['country'],
                currency=request.data['currency'],
                amount=request.data['amount']

            )

            pay_req.save()

            token = stripe.Token.create(
                card={
                    'number': pay_req.card_num,
                    'exp_month': pay_req.exp_month,
                    'exp_year': pay_req.exp_year,
                    'cvc': pay_req.cvc_num
                }
            )

            charge = stripe.Charge.create(
                source=token,
                amount=pay_req.amount,
                currency=pay_req.currency,
                description=pay_req.description,
                receipt_email=pay_req.email
            )

            resp_obj = Pay_Response.objects.create(
                id_response=charge['id'],
                currency=charge['currency'],
                country=charge['source']['country'],
                amount=charge['amount'],
                recip_mail=charge['receipt_email'],
                description=charge['description'],
                paid=charge['paid'],
                refunded=charge['refunded'],
                card_last4=charge['source']['last4']
            )
            resp_obj.save()


            print(charge)
        return super(MakePaymentView, self).create(request, *args, **kwargs)


