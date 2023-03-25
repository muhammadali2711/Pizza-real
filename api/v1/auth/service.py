import requests
from api.models import ServerTokens


def sms_sender(mobile, otp):
    token = ServerTokens.objects.get(key="sms")
    txt = f"sizning maxfiy codingiz {otp}, (uz). Bu codeni hech kimga bermang"

    url = "https://notify.eskiz.uz/api/message/sms/send"
    params = {
        "mobile_phone": mobile,
        "message": txt,
        "from": 4546,
        "callback_url": "http://0000.uz/test.php"

    }
    headers = {
        "Authorization": f"Bearer {token.token}"
    }

    response = requests.post(url, data=params, headers=headers)
    return response.json()

