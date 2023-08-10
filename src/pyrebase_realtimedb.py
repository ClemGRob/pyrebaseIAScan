import pyrebase
import pyrebase_config

firebase = pyrebase.initialize_app(pyrebase_config.pirebaseConfig)


db = firebase.database()
data = {"test": "ok"}


# db.push(data)
# db.child("test").set(data)
# db.child("test").update({"test": "oko", "test2" : "yup"})
# db.child("test").remove()
# a = db.child("test").get()
# for i in a.each():
#     print(i.val())
#     print(i.key())
#     print()