from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout


class UserMiddleware01:

    @staticmethod
    def hash_password(password):
        return make_password(password)

    @staticmethod
    def authenticate_user(request, username, password):
        user = authenticate(request, username=username, password=password)
        return user

    @staticmethod
    def login_user(request, user):
        if user is not None:
            login(request, user)

    @staticmethod
    def logout_user(request):
        logout(request)


