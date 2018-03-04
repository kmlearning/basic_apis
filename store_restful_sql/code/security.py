from user import User


def authenticate(username, password):
    """ Given username and password, return user """
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    """
    Takes in contents of JWT token and extracts user id
    Returns specific user matching payload
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)