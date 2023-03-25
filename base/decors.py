from rest_framework.response import Response


def check_method_and_params(funk):
    def wrapper(self, requests, pk=None, *args, **kwargs):
        method = requests.data.get("method")
        params = requests.data.get("params")
        if method is None:
            return Response({
                "Error": "Method kiritilmagan"
            })
        if params is None:
            return Response({
                "Error": "params kiritilmagan"
            })
        a = funk(self, requests, *args, **kwargs)
        return a
    return wrapper


def method_check(method, methods):
    return False if method not in methods else True

