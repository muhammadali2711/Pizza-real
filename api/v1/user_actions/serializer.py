from rest_framework import serializers
from Site.models import Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        exclude = ("summa",)

