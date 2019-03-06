import logging
import stripe
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import charge_create_serializer
from django.conf import settings

from ivrpayments.models import Pay_Request, Pay_Response

request_log = logging.getLogger('fileRequest')
response_log = logging.getLogger('fileResponse')
debug_log = logging.getLogger('debug')


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
            card = request.data['card_num']
            masked_card = card.replace(card[0:-4],'X'*len(card[0:-4]))
            pay_req = Pay_Request.objects.create(
                name=request.data['name'],
                email=request.data['email'],
                phone=request.data['phone'],
                card_num=masked_card,
                cvc_num=request.data['cvc_num'].replace(request.data['cvc_num'],'X'*len(request.data['cvc_num'])),
                exp_month=request.data['exp_month'],
                exp_year=request.data['exp_year'],
                description=request.data['description'],
                country=request.data['country'],
                currency=request.data['currency'],
                amount=request.data['amount']

            )
            # Check for any error in the card information
            try:
                token = stripe.Token.create(
                    card={
                        'number': request.data['card_num'],
                        'exp_month': pay_req.exp_month,
                        'exp_year': pay_req.exp_year,
                        'cvc': request.data['cvc_num']
                    }
                )

                charge = stripe.Charge.create(
                    source=token,
                    amount=pay_req.amount,
                    currency=pay_req.currency,
                    description=pay_req.description,
                    receipt_email=pay_req.email
                )

                if charge is not None:
                    try:
                        pay_req.cvc_num = 'XXX'
                        last4 = pay_req.card_num[:-4]
                        pay_req.card_num = pay_req.card_num[0:-4].replace('X') + last4
                        pay_req.save()
                        resp_obj = Pay_Response(
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
                        request_log.info(pay_req)
                        response_log.info(resp_obj)
                    except(Http404):
                        debug_log.debug('Data not found ' + pay_req)
                    except:

                        debug_log.log("Cannot save objects, invalid data \nrequest:",
                                      + pay_req + '\nresponse' + resp_obj)



                else:
                    debug_log.debug("Error processing charge: " + charge)

            except:
                debug_log.debug('Card information is not valid')
                debug_log.debug(token)

            # if the charge is completed, save the request made and the response received

        return Response(status=status.HTTP_201_CREATED)
