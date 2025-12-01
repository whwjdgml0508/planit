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
            logger.error(f"회원가입 중 오류 발생 - {str(e)}")
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
        
        # 사용자 통계 정보 추가
        context.update({
            'total_subjects': getattr(user, 'subjects', []),  # 시간표 앱에서 구현 예정
            'completed_tasks': 0,  # 플래너 앱에서 구현 예정
            'community_posts': 0,  # 커뮤니티 앱에서 구현 예정
            'study_hours': 0,  # 플래너 앱에서 구현 예정
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
        messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '프로필 업데이트 중 오류가 발생했습니다.')
        return super().form_invalid(form)
