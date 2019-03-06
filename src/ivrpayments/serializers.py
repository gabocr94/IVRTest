from rest_framework import serializers

from ivrpayments.models import Pay_Request


class charge_create_serializer(serializers.ModelSerializer):
    class Meta:
        model = Pay_Request
        exclude = ('date', 'id_request')


