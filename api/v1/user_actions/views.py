from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Site.models import Product, Basket, Size, LikeDislike, Category
from base.decors import check_method_and_params
from base.formats import add_basket_format
from base.formats import user_format
from base.helper import Bearer


class UserActions(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Bearer,)

    @check_method_and_params
    def post(self, requests, pk=None, *args, **kwargs):
        method = requests.data.get("method")
        params = requests.data.get("params")

        if method == "AddBasket":
            nott = "size_id" if "size_id" not in params else "product_id" if "product_id" not in params else None
            if nott:
                return Response({
                    "Error": f"params.{nott} kiritilmagan!"
                })

            pro = Product.objects.filter(pk=params["product_id"]).first()
            if not pro:
                return Response({
                    "Error": "bunaqa product topilmadi!"
                })

            sizes = Size.objects.filter(pk=params["size_id"]).first()

            if not sizes:
                return Response({
                    "Error": "bunaqa sizes topilmadi!"
                })
            basket = Basket.objects.get_or_create(user=requests.user, product_id=sizes.id)
            basket[0].quantity = params.get("quantity", 1)
            basket[0].save()

            return Response({
                "data": add_basket_format(basket[0])
            })

        elif method == "del.basket":
            nott = "basket_id" if "basket_id" not in params else None
            if nott:
                return Response({
                    "Error": f"params.{nott} kiritilmagan!"
                })
            basket = Basket.objects.filter(pk=params["basket_id"]).first()
            if not basket:
                return Response({"Error": "Bunaqa basket yo'q!"})
            basket.delete()
            return Response({"Success": "Basket was deleted!"})



        elif method == "likes":
            if "type" not in params or "product_id" not in params:
                return Response({
                    "Error": "params to'liq emas"
                })
            product = Product.objects.filter(pk=params.get("product_id")).first()
            if not product:
                return Response({
                    "Error": "Bunday product yo'q"
                })

            like = LikeDislike.objects.get_or_create(product=product, user=requests.user)[0]
            like.dislike = True if params['type'] == "dislike" else False
            like.like = True if params['type'] == "like" else False
            like.save()
            return Response({
                "Success": f"{params['type']}d"
            })




        else:
            return Response({
                "Error": "Bunaqa method yo'q"
            })

    def get(self, requests, pk=None, *args, **kwargs):
        if pk:
            try:
                result = add_basket_format(Basket.objects.get(pk=pk))
            except:
                result = {"Error": "Bunaqa basket_id yo'q"}

        else:
            result = [add_basket_format(x) for x in Basket.objects.filter(user=requests.user)]
        if not result:
            result = {"Error": "Databazada hech qanday ma'lumot yo'q"}

        result = {
            "sum": sum([i['price'] for i in result]),
            "data": result,
        }
        return Response(result)


class UserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (Bearer,)

    def get(self, requests, *args, **kwargs):
        user_info = user_format(requests.user)
        return Response({
            "user_info": user_info
        })

    @check_method_and_params
    def post(self, requests, pk=None, *args, **kwargs):
        method = requests.data.get("method")
        params = requests.data.get("params")

        if method == "user_change_pass":
            nott = "old" if "old" not in params else "new" if 'new' not in params else None
            if nott:
                return Response({
                    "Error": f"{nott} section is not filled"
                })
            if len(params["new"]) < 8:
                return Response({
                    "Error": "Parol 8 xonadan kam!"
                })

            if params["new"].isalpha():
                return Response({
                    "Error": "Parol faqat harfdan iborat bo'lib qoldi"
                })

            if params["new"].isdigit():
                return Response({
                    "Error": "Parol faqat sonlardan iborat bo'lib qoldi"
                })

            if not requests.user.check_password(params['old']):
                return Response({"Error": "Old password is incorrect!"})

            if params["new"] == params['old']:
                return Response({"Error": "New password is the same with old password!"})

            user_info = user_format(requests.user)
            requests.user.set_password(params['new'])
            requests.user.save()
            return Response({
                "Status": "parol was changed successfully!",
                "user": user_info
            })
