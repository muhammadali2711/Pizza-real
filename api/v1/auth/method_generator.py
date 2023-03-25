import random
import uuid
import datetime

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from api.models import User, OTP
from api.v1.auth.service import sms_sender
from base.helper import code_decoder


def reg(self, requests, params):
    nott = "phone" if "phone" not in params else "password" if "password" not in params else None
    if nott:
        return Response({
            "Error": f"params.{nott} polyasi to'ldirilmagan"
        })

    phone = params.get("phone")
    user = User.objects.filter(phone=phone).first()

    if user:
        return Response({
            "Error": "Bu raqamdan ro'yxatga o'tilgan!"
        })

    serializer = self.get_serializer(data=params)
    serializer.is_valid(raise_exception=True)
    root = serializer.create(serializer.data)
    root.set_password(params["password"])
    root.save()

    token = Token.objects.get_or_create(user=root)[0]
    return Response({
            "token": f"{token.key}"
        })


def log(self, requests, params):
    nott = "phone" if "phone" not in params else "password" if "password" not in params else None
    if nott:
        return Response({
            "Error": f"params.{nott} polyasi to'ldirilmagan"
        })

    phone = params.get("phone")
    user = User.objects.filter(phone=phone).first()

    if not user:
        return Response({
            "Error": "Bunaqa foydalanuvchi yo'q"
        })

    if not user.check_password(params["password"]):
        return Response({
            "Error": "Parol noto'g'ri"
        })

    token = Token.objects.get_or_create(user=user)[0]

    return Response({
            "token": f"{token.key}"
        })


def step_one(self, requests, params):
    nott = "phone" if "phone" not in params else None
    if nott:
        return Response({
            "Error": f"params.{nott} polyasi to'ldirilmagan"
        })

    code = random.randint(10000, 99999)
    key = f"{uuid.uuid4().__str__()}$" + str(code) + "$" + uuid.uuid1().__str__()
    # sms = sms_sender(params['phone'], code)
    # if sms.get('status') != 'waiting':
    #     return Response({
    #         "Error": "Sms xizmatda qandaydir muammo bor",
    #         "data": sms
    #     })

    root = OTP()
    root.phone = params['phone']
    root.key = code_decoder(key)
    root.save()

    return Response({
        "otp": code,
        "token": root.key
    })



def step_two(self, requests, params):
    nott = "otp" if "otp" not in params else "token" if "token" not in params else None
    if nott:
        return Response({
            "Error": f"params.{nott} polyasi to'ldirilmagan"
        })

    otp = OTP.objects.filter(key=params['token']).first()
    if not otp:
        return Response({
            "Error": "token noto'g'ri!"
        })

    otp.state = "step_two"
    otp.save()
    now = datetime.datetime.now(datetime.timezone.utc)
    cr = otp.created_at
    if (now - cr).total_seconds() > 120:
        otp.is_expired = True
        otp.save()
        return Response({
            "Error": f"Kod eskirgan"
        })

    if otp.is_expired:
        return Response({
            "Error": "token eskirgan!"
        })

    otp_key = code_decoder(otp.key, decode=True)
    key = otp_key.split("$")[1]
    if str(key) != str(params['otp']):
        otp.tries += 1
        if otp.tries >= 3:
            otp.is_expired = True

        otp.save()
        return Response({
            "Error": "Xato OTP"
        })
    user = User.objects.filter(phone=otp.phone).first() or User.objects.filter(
        phone="+" + otp.phone).first()

    otp.state = "confirmed"
    otp.save()
    if user:
        return Response({
            "is_registered": True
        })
    else:
        return Response({
            "is_registered": False
        })




