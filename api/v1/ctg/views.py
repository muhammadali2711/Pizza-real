from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.response import Response
from Site.models import Category
from base.formats import ctg_format


class CategoryView(DestroyAPIView):
    queryset = Category.objects.all()
    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                result = ctg_format(Category.objects.get(pk=pk))
            except:
                result = {"Error": "Bunaqa ctg_id yo'q"}

        else:
            result = [ctg_format(x) for x in Category.objects.all()]
        return Response(result)

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({
                "Success": 'Deleted'
            })
        except Exception as r:
            return Response({
                "Error": f"Bunaqa ctg_id yo'q, {r}"
            })
