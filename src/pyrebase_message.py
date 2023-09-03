import pyrebase
import config as pyrebase_config
from error import err
from pyfcm import FCMNotification


def send_message(API_KEY, DEVICE_TOKEN,message_title,message_body,data_message):
    push_service = FCMNotification(api_key=API_KEY)
    try:
        return push_service.notify_single_device(
        registration_id=DEVICE_TOKEN,
        message_title=message_title,
        message_body=message_body,
        data_message=data_message
        )
    except Exception as e:
        return e
     