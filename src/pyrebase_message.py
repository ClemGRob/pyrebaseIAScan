import pyrebase
import config as pyrebase_config
from error import err
from pyfcm import FCMNotification


def send_message(API_KEY:str, DEVICE_TOKEN:str,message_title:str,message_body:str,data_message:dict):
    """send a message to a device

    Args:
        API_KEY (str): API_key of the server
        DEVICE_TOKEN (str): device's token who will get the message
        message_title (str): message's tittle
        message_body (str): message's body
        data_message (dict): message's content

    Returns:
        _type_: _description_
    """
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
     