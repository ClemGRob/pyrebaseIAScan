import pyrebase
import config as pyrebase_config
from error import err



def create_auth():
    firebase = pyrebase.initialize_app(pyrebase_config.pirebaseConfig)
    return firebase.auth()

def signup(auth,email, passwd):
    try:
        user = auth.create_user_with_email_and_password(email, passwd)
    except Exception as e:
        print(err.EMAIL_ALREADY_EXISTE+"  "+str(e))

def login(auth,email, passwd):
    try:
        return auth.sign_in_with_email_and_password(email, passwd)
    except Exception as e:
        print(err.EMAIL_ALREADY_EXISTE+"  "+str(e))
        return e

