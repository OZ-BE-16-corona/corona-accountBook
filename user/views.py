from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)
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
            return Response(
                {"detail": "token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = get_user_id_from_token(token)
        except SignatureExpired:
            return Response(
                {"detail": "token expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(user_id=user_id).first()
        if not user:
            return Response(
                {"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.is_active:
            return Response(
                {"message": "이미 인증된 사용자입니다."}, status=status.HTTP_200_OK
            )

        user.is_active = True
        user.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "이메일 인증 완료"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, access_token, refresh_token)
        return response


def _set_auth_cookies(response, access_token: str, refresh_token: str):
    # settings에 없으면 기본값
    secure = getattr(settings, "JWT_COOKIE_SECURE", False)
    samesite = getattr(settings, "JWT_COOKIE_SAMESITE", "Lax")
    domain = getattr(settings, "JWT_COOKIE_DOMAIN", None)
    path = getattr(settings, "JWT_COOKIE_PATH", "/")

    response.set_cookie(
        "access",
        access_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        domain=domain,
        path=path,
        max_age=60 * 15,  # access 15분
    )
    response.set_cookie(
        "refresh",
        refresh_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        domain=domain,
        path=path,
        max_age=60 * 60 * 24 * 7,  # refresh 7일
    )


def _clear_auth_cookies(response):
    samesite = getattr(settings, "JWT_COOKIE_SAMESITE", "Lax")
    domain = getattr(settings, "JWT_COOKIE_DOMAIN", None)
    path = getattr(settings, "JWT_COOKIE_PATH", "/")

    response.delete_cookie("access", domain=domain, path=path, samesite=samesite)
    response.delete_cookie("refresh", domain=domain, path=path, samesite=samesite)


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)

            # ✅ 회전: 새 refresh를 만들기 위해 "set_jti / set_exp" 등 내부 로직을 쓰는 방식도 있지만
            # 가장 깔끔한 건 SimpleJWT의 기본 TokenRefreshSerializer를 쓰는 거야.
            # 지금 구조(커스텀 뷰) 유지하면서 간단히 처리하려면 아래처럼 “새 refresh 발급”으로 가자:

            user_id = refresh.get("user_id")
            if not user_id:
                raise Exception("invalid refresh payload")

            user = User.objects.get(user_id=user_id)

            new_refresh = RefreshToken.for_user(user)
            new_access = str(new_refresh.access_token)

            # ✅ 기존 refresh는 블랙리스트(로그아웃이 아니라 refresh 시점에도)
            try:
                refresh.blacklist()
            except Exception:
                pass

        except Exception:
            return Response(
                {"detail": "invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response({"message": "토큰 재발급 성공"}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, new_access, str(new_refresh))
        return response


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # ✅ 블랙리스트 등록
            except Exception:
                # 토큰이 이미 만료/잘못됨/이미 블랙리스트 등이어도
                # 로그아웃은 "성공"으로 처리하는 게 보통 UX 좋음
                pass

        response = Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        _clear_auth_cookies(response)  # ✅ 쿠키도 지워주기(권장)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    # ✅ 내 정보 조회
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ✅ 회원정보 수정: PATCH 권장(부분 수정)
    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            UserProfileSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    # ✅ PUT도 지원하고 싶으면(전체 교체 의미) - user_name만 받게 강제
    def put(self, request):
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            UserProfileSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    # ✅ 유저 삭제(탈퇴) - 실무적으로는 "소프트 삭제" 추천
    def delete(self, request):
        user = request.user

        # 소프트 삭제: is_active 끄고, unique 충돌 방지용 email 변경(선택)
        user.is_active = False
        user.email = f"deleted_{user.user_id}@deleted.local"
        user.user_name = f"deleted_{user.user_id}_{int(timezone.now().timestamp())}"
        user.save(update_fields=["is_active", "email", "user_name", "updated_at"])

        response = Response(
            {"message": "Deleted successfully"}, status=status.HTTP_200_OK
        )

        # 로그아웃과 같이 쿠키 제거(강추)
        try:
            _clear_auth_cookies(response)  # 너희가 이미 쓰는 쿠키 삭제 함수
        except Exception:
            pass

        return response
