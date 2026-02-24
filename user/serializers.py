from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "user_name", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def validate_user_name(self, value):
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("이미 사용 중인 유저명입니다.")
        return value

    def create(self, validated_data):
        # ✅ UserManager.create_user() 경유 → set_password()로 해시 저장
        user = User.objects.create_user(
            email=validated_data["email"],
            user_name=validated_data["user_name"],
            password=validated_data["password"],
        )
        return user