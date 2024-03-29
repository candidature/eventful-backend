from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    print ("I AM IN AUTHENTICATE")
    #user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    print("I AM in IDENTITY", user_id)
    user = UserModel.find_by_id(user_id)
    return user
