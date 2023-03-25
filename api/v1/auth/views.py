from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.models import User
from api.v1.auth import method_generator
from api.v1.auth.serializer import UserSerializer
from base.decors import check_method_and_params, method_check


class AuthView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    @check_method_and_params
    def post(self, request, *args, **kwargs):
        data = request.data

        method = data.get('method')
        params = data.get('params')

        a = method_check(method, ['reg', 'log', 'step.one', 'step.two'])

        if not a:
            return Response({
                "Error": "Bunday method yo'q"
            })
        try:
            funk = getattr(method_generator, method.replace(".", "_"))
            mapp = map(funk, [self], [request], [params])
            return list(mapp)[0]

        except Exception as e:
            return Response({
                "Error": f"Xatolik bor {e}"
            })
