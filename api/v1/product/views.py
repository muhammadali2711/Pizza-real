from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from Site.models import Product
from api.v1.product.serializer import ProductSerializer
from base.formats import product_format


class ProductView(UpdateAPIView, CreateAPIView, DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                result = product_format(Product.objects.get(pk=pk))
            except:
                result = {"Error": "Bunaqa product_id yo'q"}

        else:
            result = [product_format(x) for x in Product.objects.all()]
        return Response(result)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({
                "Success": 'Deleted'
            })
        except:
            return Response({
                "Error": "Bunaqa product_id yo'q"
            })

