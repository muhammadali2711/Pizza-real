from rest_framework import serializers
from Site.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"