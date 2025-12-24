from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes, parser_classes # ✅ parser_classes 추가
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils import timezone
import uuid
from rest_framework.parsers import MultiPartParser, FormParser # ✅ Parser들 추가
from django.shortcuts import get_object_or_404
from .models import Follow, UserSetting
from .serializers import (
    SignupSerializer,
    UserSerializer,
    ProfileUpdateSerializer,
    ThemeSerializer,
    FollowToggleResultSerializer,
    WithdrawSerializer,
    FindUsernameSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


def _issue_tokens(user: User):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
        {"message": "회원가입 성공", "user": UserSerializer(user).data},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    print("LOGIN raw data:", request.data)
    print("LOGIN keys:", list(request.data.keys()))

    identifier = (request.data.get("username") or request.data.get("email") or "").strip()
    password = request.data.get("password", "")

    if not identifier or not password:
        return Response(
            {"detail": "username(email)과 password는 필수입니다."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1) username으로 먼저 시도
    user = authenticate(request, username=identifier, password=password)

    # 2) 실패하면 email로 유저 찾고 username으로 authenticate
    if not user:
        u = User.objects.filter(email__iexact=identifier).first()
        if u:
            user = authenticate(request, username=u.username, password=password)

    # user가 만들어졌을 수도 있으니, 실패 처리 전에 체크
    if user and not user.is_active:
        return Response({"detail": "비활성화된 계정입니다."}, status=status.HTTP_403_FORBIDDEN)

    if not user:
        return Response(
            {"detail": "아이디(또는 이메일) / 비밀번호가 올바르지 않습니다."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({"user": UserSerializer(user).data, "tokens": _issue_tokens(user)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


# backend/accounts/views.py

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser]) # ✅ 이미지 파일 전송을 위해 필수 추가!
def update_profile(request):
    user = request.user
    
    # 1. 비밀번호 변경 로직 (입력값이 있을 때만 실행)
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    
    if old_password and new_password:
        if not user.check_password(old_password):
            return Response({"detail": "현재 비밀번호가 일치하지 않습니다."}, status=400)
        user.set_password(new_password)
        user.save()
        # 비밀번호 변경 후 세션/토큰 유지를 위해 필요한 경우 처리 (SimpleJWT는 재로그인 필요 없음)

    # 2. 프로필 정보 및 이미지 업데이트
    # partial=True를 주어 일부 필드만 넘어와도 허용합니다.
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(UserSerializer(user).data)
    
    return Response(serializer.errors, status=400)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_theme(request):
    setting, _ = UserSetting.objects.get_or_create(user=request.user)
    serializer = ThemeSerializer(setting, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"theme": setting.theme}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def user_profile(request, username):
    target = User.objects.filter(username=username).first()
    if not target:
        return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    data = UserSerializer(target).data

    # ✅ 로그인 상태면 내가 팔로우 중인지 추가 제공
    is_following = False
    if getattr(request.user, "is_authenticated", False):
        is_following = Follow.objects.filter(from_user=request.user, to_user=target).exists()

    data["is_following"] = is_following
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_toggle(request, username):
    if request.user.username == username:
        return Response({"detail": "자기 자신은 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    target = User.objects.filter(username=username).first()
    if not target:
        return Response({"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    rel = Follow.objects.filter(from_user=request.user, to_user=target).first()
    if rel:
        rel.delete()
        is_following = False
    else:
        Follow.objects.create(from_user=request.user, to_user=target)
        is_following = True

    result = {
        "is_following": is_following,
        "followers_count": Follow.objects.filter(to_user=target).count(),
        "following_count": Follow.objects.filter(from_user=target).count(),
    }
    return Response(FollowToggleResultSerializer(result).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def social_login_placeholder(request, provider):
    allowed = ["google", "kakao", "apple", "x", "line"]
    if provider not in allowed:
        return Response({"detail": "지원하지 않는 provider입니다."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"detail": f"{provider} 소셜 로그인은 다음 단계에서 실제 연동 로직을 붙입니다."},
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )



# [추가] 팔로워/팔로잉 목록 조회
@api_view(['GET'])
@permission_classes([AllowAny]) # 비로그인 유저도 볼 수 있게 하려면 AllowAny
def user_follow_list(request, username, type):
    target_user = get_object_or_404(User, username=username)
    
    if type == 'followers':
        # 나를 팔로우하는 사람들 (Follow 테이블의 from_user들)
        relations = Follow.objects.filter(to_user=target_user).select_related('from_user')
        users = [r.from_user for r in relations]
    elif type == 'following':
        # 내가 팔로우하는 사람들 (Follow 테이블의 to_user들)
        relations = Follow.objects.filter(from_user=target_user).select_related('to_user')
        users = [r.to_user for r in relations]
    else:
        return Response(status=400)

    # 필요한 정보만 간단히 리턴 (UserSerializer 재사용 또는 직접 구성)
    data = []
    for u in users:
        data.append({
            'id': u.id,
            'username': u.username,
            'profile_image': u.profile_image.url if u.profile_image else None,
            'email': u.email
        })
    
    return Response(data)

# backend/accounts/views.py (아래에 추가)

def _frontend_base_url(request):
    """
    비번 재설정 링크 생성용.
    1) settings.FRONTEND_BASE_URL 있으면 사용
    2) 없으면 요청 Origin 사용
    3) 둘 다 없으면 localhost로 fallback
    """
    base = getattr(settings, "FRONTEND_BASE_URL", None)
    if base:
        return base.rstrip("/")
    origin = request.headers.get("Origin")
    if origin:
        return origin.rstrip("/")
    return "http://localhost:5173"


def _send_email_safely(subject: str, message: str, to_email: str):
    """
    개발 단계에서는 콘솔 이메일 백엔드면 print로 확인 가능.
    운영에서는 SMTP 세팅 필요.
    """
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
    send_mail(subject, message, from_email, [to_email], fail_silently=True)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def withdraw(request):
    """
    ✅ 회원 탈퇴(Soft delete 권장)
    - 일반 계정: password 재확인 필수
    - 소셜/비번없는 계정: password 없이 탈퇴 가능
    - 개인정보 마스킹 + 계정 비활성화
    """
    ser = WithdrawSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    password = (ser.validated_data.get("password") or "").strip()

    user = request.user

    # 일반 계정이면 비밀번호 확인 요구
    if user.has_usable_password():
        if not password:
            return Response({"detail": "비밀번호 확인이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response({"detail": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # 팔로우 관계 정리(원하면 유지해도 되는데, 보통 지움)
        Follow.objects.filter(from_user=user).delete()
        Follow.objects.filter(to_user=user).delete()

        # 개인정보 마스킹 + 비활성화
        user.is_active = False

        # username/email unique라서 충돌 방지용으로 바꿔둠(재가입 가능하게)
        suffix = uuid.uuid4().hex[:10]
        user.username = f"deleted_{user.id}_{suffix}"
        user.email = f"deleted_{user.id}_{suffix}@deleted.local"
        user.name = ""
        user.birth_date = None
        user.gender = None

        # 프로필 이미지 제거
        user.profile_image = None

        # 비번 unusable 처리
        user.set_unusable_password()

        # 선택: 탈퇴 시각 기록하고 싶으면 모델에 필드 추가 후 저장
        user.save(update_fields=[
            "is_active", "username", "email", "name", "birth_date", "gender",
            "profile_image", "password"
        ])

    return Response({"message": "탈퇴 처리되었습니다."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def find_username(request):
    """
    ✅ 아이디 찾기
    - 응답으로 존재 여부를 절대 드러내지 않음
    - 조건이 맞으면 이메일로 username 발송
    """
    ser = FindUsernameSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    email = ser.validated_data["email"].strip()
    birth_date = ser.validated_data.get("birth_date")

    user = User.objects.filter(email__iexact=email, is_active=True).first()

    # birth_date를 받았다면 추가 검증
    if user and birth_date and user.birth_date != birth_date:
        user = None

    # user가 있을 때만 이메일 발송(그래도 응답은 동일하게)
    if user:
        subject = "[혜성(The Comet)] 아이디(Username) 안내"
        message = (
            "요청하신 아이디 안내입니다.\n\n"
            f"- 아이디(username): {user.username}\n\n"
            "본인이 요청하지 않았다면 이 메일을 무시하세요."
        )
        _send_email_safely(subject, message, user.email)

    return Response(
        {"message": "입력하신 정보와 일치하는 계정이 있으면 이메일로 안내했습니다."},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    ✅ 비밀번호 재설정 요청
    - 이메일 입력 → uid/token 생성 → 프론트 재설정 페이지 링크 이메일 발송
    - 응답은 항상 동일(계정 존재 여부 숨김)
    """
    ser = PasswordResetRequestSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    email = ser.validated_data["email"].strip()
    user = User.objects.filter(email__iexact=email, is_active=True).first()

    if user:
        token_gen = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_gen.make_token(user)

        base = _frontend_base_url(request)
        # 프론트 라우트 예시: /reset-password?uid=...&token=...
        reset_link = f"{base}/reset-password?uid={uid}&token={token}"

        subject = "[혜성(The Comet)] 비밀번호 재설정 안내"
        message = (
            "비밀번호 재설정 요청을 받았습니다.\n\n"
            "아래 링크에서 새 비밀번호를 설정해주세요:\n"
            f"{reset_link}\n\n"
            "본인이 요청하지 않았다면 이 메일을 무시하세요."
        )
        _send_email_safely(subject, message, user.email)

    return Response(
        {"message": "해당 이메일의 계정이 존재하면 재설정 링크를 전송했습니다."},
        status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    ✅ 비밀번호 재설정 확정
    - uid/token 검증 → new_password 저장
    """
    ser = PasswordResetConfirmSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    uid = ser.validated_data["uid"]
    token = ser.validated_data["token"]
    new_password = ser.validated_data["new_password"]

    # uid 복호화 → user 찾기
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.filter(pk=user_id, is_active=True).first()
    except Exception:
        user = None

    if not user:
        return Response({"detail": "유효하지 않은 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

    token_gen = PasswordResetTokenGenerator()
    if not token_gen.check_token(user, token):
        return Response({"detail": "토큰이 만료되었거나 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save(update_fields=["password"])

    return Response({"message": "비밀번호가 변경되었습니다. 다시 로그인해주세요."}, status=status.HTTP_200_OK)



