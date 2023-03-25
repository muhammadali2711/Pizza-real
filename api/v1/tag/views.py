from rest_framework.generics import GenericAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from Site.models import Product, ProductTag, Tag
from api.v1.tag.serializer import TagSerializer
from base.formats import tag_format


class TagView(UpdateAPIView, CreateAPIView, DestroyAPIView):
    serializer_class = TagSerializer
    queryset = ProductTag.objects.all()

    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                result = tag_format(Tag.objects.get(pk=pk))
            except:
                result = {"Error": "Bunaqa tag_id yo'q"}

        else:
            result = [tag_format(x) for x in Tag.objects.all()]
        return Response(result)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({
                "Success": 'Deleted'
            })
        except:
            return Response({
                "Error": "Bunaqa tag_id yo'q"
            })
