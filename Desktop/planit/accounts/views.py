from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm

User = get_user_model()

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
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'{user.get_full_name()}님, 회원가입을 환영합니다!')
        return response
    
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
