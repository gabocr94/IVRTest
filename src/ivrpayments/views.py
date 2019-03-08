import logging
import stripe
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from stripe.error import CardError, APIConnectionError, InvalidRequestError, StripeError

from .serializers import charge_create_serializer
from django.conf import settings
from ivrpayments.models import Pay_Response

data_log = logging.getLogger('stripedata')
debug_log = logging.getLogger('filedebug')


class MakePaymentView(CreateAPIView):
    serializer_class = charge_create_serializer

    def mask_ccnum(self, cc_num):
        """
        masks credit card number
        :param cc_num:
        :return: the masked credit card with last 4 numbers visible
        """
        cc_num = cc_num.replace(cc_num[0:-4], 'X' * len(cc_num[0:-4]))
        return cc_num

    def post(self, request, *args, **kwargs):
        """
        Creates the request and response model to the database while sending and receiving data from stripe
        :param request: It has the data from the rest form on the view
        :param args:
        :param kwargs:
        :return: HTTP code status 201 on create or other HTTP error codes
        """
        if request.method == 'POST':

            # serializer takes post data

            stripe.api_key = settings.STRIPE_SECRET_KEY
            serializer = self.serializer_class(data=request.data)

            try:
                if serializer.is_valid():
                    # Saving and logging the request

                    # Create the token needed fpr the stripe charge
                    token = stripe.Token.create(
                        card={
                            'number': serializer.validated_data.get('card_num'),
                            'exp_month': serializer.validated_data.get('exp_month'),
                            'exp_year': serializer.validated_data.get('exp_year'),
                            'cvc': serializer.validated_data.get('cvc_num'),
                        }
                    )

                    # mask the information once is used and then save
                    serializer.validated_data['card_num'] = self.mask_ccnum(serializer.validated_data['card_num'])
                    serializer.validated_data['cvc_num'] = "XXX"
                    serializer.save()
                    data_log.info(serializer.validated_data)
                    charge = stripe.Charge.create(
                        source=token,
                        amount=serializer.validated_data.get('amount'),
                        currency=serializer.validated_data.get('currency'),

                    )
                    # Transform charge response into our desired model to be saved in db
                    resp_obj = Pay_Response(
                        id_response=charge['id'],
                        currency=charge['currency'],
                        amount=charge['amount'],
                        paid=charge['paid'],
                        refunded=charge['refunded'],
                        card_last4=charge['source']['last4']
                    )
                    resp_obj.save()
                    data_log.info(resp_obj)
                else:
                    return Response(data='Information is not correct', status=status.HTTP_400_BAD_REQUEST)

            # Check for any error in the card information or code

            except StripeError as e:
                debug_log.debug(e)
                return Response(data='Error, please verify your card information',
                                status=status.HTTP_402_PAYMENT_REQUIRED)
            except ValidationError as e:
                debug_log.debug(e)
                return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                debug_log.debug(e)
                return Response(data=e, status=status.HTTP_400_BAD_REQUEST)

            return Response(data=charge, status=status.HTTP_201_CREATED)
        else:
            return Response(data='Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
