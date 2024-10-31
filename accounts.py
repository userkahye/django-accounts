
from .models import Client
from .userauth import UserMiddleware01

class AccountService01:

    @staticmethod
    def save_user_with_hashed_password(username, password, email):
 
        hashed_password = UserMiddleware01.hash_password(password)
        user = Client(username=username, password=hashed_password, email=email)
        user.save()
        return user
