from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm

User = get_user_model()
logger = logging.getLogger(__name__)

class LoginView(BaseLoginView):
    """로그인 뷰"""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, f'{form.get_user().get_full_name()}님, 환영합니다!')
        return super().form_valid(form)

def logout_view(request):
    """로그아웃 뷰 (함수형)"""
    if request.user.is_authenticated:
        messages.info(request, '성공적으로 로그아웃되었습니다.')
        logout(request)
    return redirect('home')

class RegisterView(CreateView):
    """회원가입 뷰"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        try:
            logger.info(f"회원가입 시도 - 사용자명: {form.cleaned_data.get('username')}, 학번: {form.cleaned_data.get('student_id')}")
            
            # 사용자 저장
            user = form.save()
            logger.info(f"사용자 저장됨 - ID: {user.id}, 사용자명: {user.username}, 학번: {user.student_id}")
            
            # 회원가입 후 자동 로그인을 위해 authenticate 사용
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request=self.request, username=username, password=password)
            
            if authenticated_user:
                login(self.request, authenticated_user)
                messages.success(self.request, f'{authenticated_user.get_full_name()}님, 회원가입을 환영합니다!')
                logger.info(f"자동 로그인 성공 - {authenticated_user.username}")
            else:
                # 인증 실패 시에도 회원가입은 성공했음을 알림
                messages.success(self.request, f'{user.get_full_name()}님, 회원가입이 완료되었습니다. 로그인해주세요.')
                logger.warning(f"자동 로그인 실패, 하지만 회원가입은 성공 - {user.username}")
            
            return redirect(self.success_url)
            
        except Exception as e:
            logger.error(f"회원가입 중 오류 발생 - {str(e)}", exc_info=True)
            messages.error(self.request, f'회원가입 중 오류가 발생했습니다: {str(e)}')
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '회원가입 정보를 다시 확인해주세요.')
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, DetailView):
    """프로필 조회 뷰"""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # 등록된 과목 수 (timetable.Subject)
        from timetable.models import Subject
        total_subjects = Subject.objects.filter(user=user)
        
        # 완료된 과제 수 (planner.Task)
        from planner.models import Task, StudySession
        completed_tasks = Task.objects.filter(
            user=user,
            status='COMPLETED'
        ).count()
        
        # 커뮤니티 게시글 수 (community.Post)
        from community.models import Post
        community_posts = Post.objects.filter(
            author=user,
            is_active=True
        ).count()
        
        # 이번 주 학습시간 계산 (planner.StudySession)
        # 이번 주의 시작(월요일)과 끝(일요일) 계산
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # 월요일
        end_of_week = start_of_week + timedelta(days=6)  # 일요일
        
        # 이번 주의 학습 세션 총 시간 계산
        study_sessions = StudySession.objects.filter(
            user=user,
            start_time__date__gte=start_of_week,
            start_time__date__lte=end_of_week,
            end_time__isnull=False,  # 완료된 세션만
            duration_minutes__isnull=False  # duration_minutes가 있는 세션만
        )
        
        # 총 학습 시간 계산
        total_minutes = study_sessions.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0
        
        study_hours = round(total_minutes / 60, 1)  # 분을 시간으로 변환
        
        # 사용자 통계 정보 추가
        context.update({
            'total_subjects': total_subjects,
            'completed_tasks': completed_tasks,
            'community_posts': community_posts,
            'study_hours': study_hours,
        })
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """프로필 수정 뷰"""
    model = User
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        # 프로필 이미지 삭제 처리
        if self.request.POST.get('profile_image-clear') == 'on':
            user = form.save(commit=False)
            if user.profile_image:
                user.profile_image.delete(save=False)
                user.profile_image = None
            user.save()
            messages.success(self.request, '프로필 이미지가 제거되었습니다.')
            return redirect(self.success_url)
        
        messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '프로필 업데이트 중 오류가 발생했습니다.')
        logger.error(f"프로필 업데이트 실패 - 사용자: {self.request.user.username}, 오류: {form.errors}")
        return super().form_invalid(form)
