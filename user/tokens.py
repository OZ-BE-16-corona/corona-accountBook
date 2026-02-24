from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

_signer = TimestampSigner(salt="user-email-verify")


def make_email_verify_token(user_id: int) -> str:
    # token 형식: "<user_id>:<signature>"
    return _signer.sign(str(user_id))


def get_user_id_from_token(token: str, max_age_seconds: int = 60 * 60 * 24) -> int:
    # 기본 24시간 유효
    user_id_str = _signer.unsign(token, max_age=max_age_seconds)
    return int(user_id_str)