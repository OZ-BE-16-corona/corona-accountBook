from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.signing import BadSignature, SignatureExpired

from .models import User
from .serializers import RegisterSerializer
from .tokens import make_email_verify_token, get_user_id_from_token


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        if user.is_active:
            user.is_active = False
            user.save(update_fields=["is_active"])

        # ✅ 1) token 먼저 만들기
        token = make_email_verify_token(user.user_id)

        # ✅ 2) base_url 안전하게 가져오기
        base_url = getattr(settings, "BACKEND_BASE_URL", "http://127.0.0.1:8000")
        verify_url = f"{base_url}/api/auth/verify-email/?token={token}"

        send_mail(
            subject="[돈두세요] 이메일 인증을 완료해주세요",
            message=f"아래 링크를 눌러 이메일 인증을 완료해주세요:\n{verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "회원가입 완료. 이메일 인증 메일을 확인해주세요."},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = get_user_id_from_token(token)
        except SignatureExpired:
            return Response({"detail": "token expired"}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response({"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({"message": "이미 인증된 사용자입니다."}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "이메일 인증 완료"}, status=status.HTTP_200_OK)