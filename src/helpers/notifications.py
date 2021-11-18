from os import getenv
from pyfcm import FCMNotification

pushService = FCMNotification(getenv("FCM_API_KEY"))

def sendNotifications(title: str, body: str, tokens: list, data: object):
    result = pushService.notify_multiple_devices(
        registration_ids=tokens, 
        message_title=title, 
        message_body=body, 
        data_message=data, 
        sound="Default"
    )
    print(result)