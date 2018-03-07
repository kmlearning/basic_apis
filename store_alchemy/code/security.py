from models.user import UserModel


def authenticate(username, password):
    """ Given username and password, return user """
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    """
    Takes in contents of JWT token and extracts user id
    Returns specific user matching payload
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)