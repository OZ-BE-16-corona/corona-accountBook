from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authorization 헤더 대신 HttpOnly 쿠키에서 access 토큰을 읽어서 인증.
    """

    def authenticate(self, request):
        access_token = request.COOKIES.get("access")
        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)
        return (user, validated_token)
