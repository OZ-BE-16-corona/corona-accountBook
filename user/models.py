from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, user_name: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        if not user_name:
            raise ValueError("user_name is required")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        if password:
            user.set_password(password)  # 비밀번호 해시 생성
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, user_name: str, password: str, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email=email, user_name=user_name, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # ERD: user_id (PK)
    user_id = models.BigAutoField(primary_key=True)

    # ERD: user_name
    user_name = models.CharField(max_length=20, unique=True)

    # ERD: email
    email = models.EmailField(max_length=100, unique=True)

    # ERD: password_hash (DB 컬럼명만 맞추기)
    password = models.CharField(max_length=255, db_column="password_hash")

    # ERD: is_admin
    is_admin = models.BooleanField(default=False)

    # Django 운영용 (권장)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # ERD: created_at / updated_at
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        db_table = "user"

    def __str__(self) -> str:
        return f"{self.user_name}<{self.email}>"