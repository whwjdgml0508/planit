from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
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
        from django.db.models import Sum
        from timetable.models import Subject
        from planner.models import Task, StudySession
        from community.models import Post
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 최근 30일 기준
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # 커뮤니티 활동 통계
        context['posts_count'] = user.posts.filter(is_active=True).count()
        context['recent_posts_count'] = user.posts.filter(
            is_active=True,
            created_at__gte=thirty_days_ago
        ).count()
        context['comments_count'] = user.comments.filter(is_active=True).count()
        context['recent_comments_count'] = user.comments.filter(
            is_active=True,
            created_at__gte=thirty_days_ago
        ).count()
        
        # 플래너 활동 통계
        context['tasks_count'] = user.tasks.count()
        context['completed_tasks_count'] = user.tasks.filter(status='COMPLETED').count()
        context['recent_completed_tasks'] = user.tasks.filter(
            status='COMPLETED',
            completed_at__gte=thirty_days_ago
        ).count()
        
        # 학습 세션 통계
        study_sessions = user.study_sessions.filter(
            start_time__gte=thirty_days_ago,
            end_time__isnull=False
        )
        total_minutes = study_sessions.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0
        context['study_hours'] = round(total_minutes / 60, 1)
        context['study_sessions_count'] = study_sessions.count()
        
        # 등록된 과목 수
        context['subject_count'] = Subject.objects.filter(user=user).count()
        
        # 완료한 과제 수
        context['completed_task_count'] = Task.objects.filter(
            user=user,
            status='COMPLETED'
        ).count()
        
        # 커뮤니티 게시글 수
        context['post_count'] = Post.objects.filter(
            author=user,
            is_active=True
        ).count()
        
        # 이번주 학습시간 계산 (월요일부터 일요일까지)
        today = timezone.now().date()
        # 이번주 월요일 찾기
        start_of_week = today - timedelta(days=today.weekday())
        # 이번주 일요일 찾기
        end_of_week = start_of_week + timedelta(days=6)
        
        # 이번주 학습 세션의 총 시간 계산 (분 단위)
        weekly_study_minutes = StudySession.objects.filter(
            user=user,
            start_time__date__gte=start_of_week,
            start_time__date__lte=end_of_week,
            end_time__isnull=False
        ).aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0
        
        # 시간으로 변환
        context['weekly_study_hours'] = round(weekly_study_minutes / 60, 1) if weekly_study_minutes else 0
        
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
            logger.info(f"프로필 이미지 제거 - 사용자: {user.username}")
            return redirect(self.success_url)
        
        # 새 프로필 이미지 업로드 처리
        if 'profile_image' in self.request.FILES:
            # 기존 이미지가 있으면 삭제
            if self.request.user.profile_image:
                self.request.user.profile_image.delete(save=False)
            logger.info(f"프로필 이미지 업로드 - 사용자: {self.request.user.username}, 파일: {self.request.FILES['profile_image'].name}")
        
        # 폼을 통해 저장 (파일 포함)
        user = form.save()
        messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        logger.info(f"프로필 업데이트 성공 - 사용자: {user.username}")
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, '프로필 업데이트 중 오류가 발생했습니다.')
        logger.error(f"프로필 업데이트 실패 - 사용자: {self.request.user.username}, 오류: {form.errors}")
        return super().form_invalid(form)
