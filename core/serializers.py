from rest_framework import serializers


class CurrencyConverterSerializers(serializers.Serializer):
    convert_from = serializers.CharField(max_length=3)
    convert_into = serializers.CharField(max_length=3)
    amount = serializers.FloatField()
