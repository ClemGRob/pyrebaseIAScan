from pyfcm import FCMNotification
import pyrebase
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import config
from src.wrapper import *


firebase = pyrebase.initialize_app(config.pirebaseConfig)


API_KEY = 'AAAA1tVrxG8:APA91bHDrzJTO1faGyz7Gs2ANsSQBrZHCDLWMGnqMEUt4uJ18-7Z4ohWBooiGJnvQcxUZ4WXRjcNtbo_ImpeJG0WmmZ9YitHkoX4OFQYq1itXt8OOncF-oKX0L30wUOkNs4lC_lEd3HL'
DEVICE_TOKEN = "d4XymCvyQIy5pd9KEmOkba:APA91bGCS5T0s_cAJtzMV6ejHq58vFWR1tyZtPJjAgZy2ICiNw-kOM0oOWu6zCV_pN9ylFc0MbEWCQsbjGIY1UUH3s74Rd03DmNMKk8njO9XEcgv0eAeY_rcrWBpPg5NGKpOJSLyGxYH"



# Initialisez le client FCM
# push_service = FCMNotification(api_key=API_KEY)

# Créez un message
message_title = "message de test"
message_body = "salut"
data_message = {
    "key1": "ca ",
    "key2": "marche"
}
print(send_message(config.API_KEY, DEVICE_TOKEN,message_title,message_body,data_message))

