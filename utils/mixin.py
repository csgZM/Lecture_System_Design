from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from Login.models import UserToken


class AuthticationView(BaseAuthentication):
    def authenticate(self, request):
        token = request.get_full_path().split('/')[2]
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('认证失败')
        return (token_obj.Username_id, token_obj)

    def authenticate_header(self, request):
        pass
