# from django.contrib.auth.backends import BaseBackend
# from account.models import User

# class EmailAuthBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except User.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None



from django.contrib.auth.backends import BaseBackend
from account.models import User

class EmailOrPhoneAuthBackend(BaseBackend):
    """
    Custom authentication backend that supports login with either
    an email address or a phone number as the 'username' input.
    """

    def authenticate(self, request, username=None, password=None):
        # Guard against missing credentials
        if username is None or password is None:
            return None

        user = None

        # If the identifier contains '@', treat it as an email
        if '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        else:
            # Otherwise treat it as a phone number
            try:
                user = User.objects.get(phone__iexact=username)
            except User.DoesNotExist:
                return None

        # Check the password for the resolved user
        if user.check_password(password):
            return user

        # Invalid password
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None