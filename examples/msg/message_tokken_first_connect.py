from pyfcm import FCMNotification
import pyrebase
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config
from src.wrapper import *


firebase = pyrebase.initialize_app(config.pirebaseConfig)
db = firebase.database()
auth=firebase.auth()
user=login(auth, "password@password.password","password")


tokken = get_data(db,"token")
print(tokken)
DEVICE_NAME= list(tokken.keys())[0]
DEVICE_TOKEN = tokken[DEVICE_NAME]

message_title = "message de test"
message_body = "salut"
data_message = {
    "key1": "ca ",
    "key2": "marche"
}
print(send_message(config.API_KEY, DEVICE_TOKEN,message_title,message_body,data_message))