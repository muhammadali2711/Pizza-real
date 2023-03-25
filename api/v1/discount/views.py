from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from Site.models import Discount, Size
from api.v1.discount.serializer import DiscountSerializer
from base.formats import discount_format


class DiscountView(GenericAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()

    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                discount = Discount.objects.filter(pk=pk).first()
                result = discount_format(discount)
            except:
                result = "Mahsulot topilmadi"
            return Response({"data": result})

        else:
            result = [discount_format(i) for i in Discount.objects.all()]
            if not result:
                result = "Discountda Mahsulot umuman yo'q"
            return Response({
                "data": result
            })

