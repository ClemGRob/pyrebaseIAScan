import pyrebase
import pyrebase_config
from error import err


firebase = pyrebase.initialize_app(pyrebase_config.pirebaseConfig)
auth = firebase.auth()


def signup(email, passwd):
    try:
        user = auth.create_user_with_email_and_password(email, passwd)
    except:
        print(err.EMAIL_ALREADY_EXISTE)

def login(email, passwd):
    try:
        user = auth.sign_in_with_email_and_password(email, passwd)
    except:
        print(err.WRONG_EMAIL)

login("teofgsta@test.com", "fazzkepwd")