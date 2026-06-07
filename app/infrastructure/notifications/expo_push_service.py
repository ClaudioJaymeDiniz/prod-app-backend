import json
import urllib.request


EXPO_PUSH_URL = 'https://exp.host/--/api/v2/push/send'


async def send_expo_push_notification(token: str, title: str, body: str, data: dict | None = None):
    payload = {
        'to': token,
        'title': title,
        'body': body,
        'sound': 'default',
        'data': data or {},
    }

    request = urllib.request.Request(
        EXPO_PUSH_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response.read()
    except Exception as exc:
        print(f'Erro ao enviar push notification: {exc}')