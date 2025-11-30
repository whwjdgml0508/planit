from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class StudentIdBackend(ModelBackend):
    """
    사용자명 또는 학번으로 로그인할 수 있는 커스텀 인증 백엔드
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            # 사용자명 또는 학번으로 사용자 찾기
            user = User.objects.get(
                Q(username=username) | Q(student_id=username)
            )
        except User.DoesNotExist:
            # 사용자가 존재하지 않으면 None 반환
            return None
        except User.MultipleObjectsReturned:
            # 여러 사용자가 발견되면 첫 번째 사용자 반환
            user = User.objects.filter(
                Q(username=username) | Q(student_id=username)
            ).first()
        
        # 비밀번호 확인
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
