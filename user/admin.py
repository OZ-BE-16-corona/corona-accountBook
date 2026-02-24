from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # ✅ 정렬: id가 아니라 pk(user_id)로
    ordering = ("-user_id",)

    # ✅ 목록에서 보여줄 컬럼(존재하는 필드만)
    list_display = (
        "user_id",
        "email",
        "user_name",
        "is_staff",
        "is_active",
        "is_admin",
        "created_at",
        "updated_at",
    )

    # ✅ 이메일/닉네임/휴대폰번호로 검색 -> 휴대폰번호 필드가 없으니 제외
    # (phone_number 추가되면 여기만 추가하면 됨)
    search_fields = ("email", "user_name")

    # ✅ 관리자 여부(is_staff) + 활성화(is_active) 필터
    list_filter = ("is_staff", "is_active")

    # ✅ 어드민 여부(is_admin)는 읽기 전용
    readonly_fields = ("is_admin", "created_at", "updated_at")

    # ✅ 커스텀 유저는 username 필드가 없어서 fieldsets/ add_fieldsets 직접 지정하는게 안전
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("user_name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_admin",
                )
            },
        ),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "user_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    # 이메일로 로그인하니까 admin에서도 이메일 기준으로
    list_display_links = ("user_id", "email")
