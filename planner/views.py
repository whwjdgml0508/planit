from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task, StudySession, Goal
from .forms import TaskForm, StudySessionForm, GoalForm, TaskQuickAddForm, TaskFilterForm

class PlannerView(LoginRequiredMixin, TemplateView):
    """플래너 대시보드 뷰"""
    template_name = 'planner/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        
        # 오늘의 과제
        today_tasks = Task.objects.filter(
            user=user,
            due_date__date=today,
            status__in=['TODO', 'IN_PROGRESS']
        )
        
        # 이번 주 과제
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_tasks = Task.objects.filter(
            user=user,
            due_date__date__range=[week_start, week_end],
            status__in=['TODO', 'IN_PROGRESS']
        )
        
        # 마감일 지난 과제
        overdue_tasks = Task.objects.filter(
            user=user,
            due_date__lt=timezone.now(),
            status__in=['TODO', 'IN_PROGRESS']
        )
        
        # 최근 완료된 과제
        recent_completed = Task.objects.filter(
            user=user,
            status='COMPLETED',
            completed_at__gte=today - timedelta(days=7)
        )
        
        # 이번 주 학습 세션
        week_sessions = StudySession.objects.filter(
            user=user,
            start_time__date__range=[week_start, week_end],
            end_time__isnull=False
        )
        
        # 이번 주 총 학습시간
        total_study_minutes = week_sessions.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0
        
        # 활성 목표
        active_goals = Goal.objects.filter(
            user=user,
            start_date__lte=today,
            end_date__gte=today,
            is_achieved=False
        )
        
        # 통계
        task_stats = {
            'total': Task.objects.filter(user=user).count(),
            'completed': Task.objects.filter(user=user, status='COMPLETED').count(),
            'in_progress': Task.objects.filter(user=user, status='IN_PROGRESS').count(),
            'overdue': overdue_tasks.count(),
        }
        
        context.update({
            'today_tasks': today_tasks,
            'week_tasks': week_tasks,
            'overdue_tasks': overdue_tasks,
            'recent_completed': recent_completed,
            'week_sessions': week_sessions,
            'total_study_hours': total_study_minutes / 60,
            'active_goals': active_goals,
            'task_stats': task_stats,
            'quick_add_form': TaskQuickAddForm(),
        })
        return context

class TaskListView(LoginRequiredMixin, ListView):
    """과제 목록 뷰"""
    model = Task
    template_name = 'planner/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        # 필터링
        form = TaskFilterForm(self.request.GET, user=self.request.user)
        if form.is_valid():
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['priority']:
                queryset = queryset.filter(priority=form.cleaned_data['priority'])
            if form.cleaned_data['category']:
                queryset = queryset.filter(category=form.cleaned_data['category'])
            if form.cleaned_data['subject']:
                queryset = queryset.filter(subject=form.cleaned_data['subject'])
            if form.cleaned_data['overdue_only']:
                queryset = queryset.filter(
                    due_date__lt=timezone.now(),
                    status__in=['TODO', 'IN_PROGRESS']
                )
        
        return queryset.select_related('subject')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET, user=self.request.user)
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    """과제 생성 뷰"""
    model = Task
    form_class = TaskForm
    template_name = 'planner/task_create.html'
    success_url = reverse_lazy('planner:task_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'"{form.instance.title}" 과제가 추가되었습니다.')
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    """과제 상세 뷰"""
    model = Task
    template_name = 'planner/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).select_related('subject')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        
        # 관련 학습 세션
        study_sessions = StudySession.objects.filter(task=task).order_by('-start_time')
        context['study_sessions'] = study_sessions
        
        return context

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """과제 수정 뷰"""
    model = Task
    form_class = TaskForm
    template_name = 'planner/task_edit.html'
    success_url = reverse_lazy('planner:task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" 과제가 수정되었습니다.')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """과제 삭제 뷰"""
    model = Task
    template_name = 'planner/task_delete.html'
    success_url = reverse_lazy('planner:task_list')
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task_title = task.title
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'"{task_title}" 과제가 삭제되었습니다.')
        return result

class TaskToggleView(LoginRequiredMixin, TemplateView):
    """과제 상태 토글 뷰 (AJAX)"""
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(Task, id=task_id, user=request.user)
        
        # 상태 토글
        if task.status == 'COMPLETED':
            task.status = 'TODO'
            task.progress = 0
            message = f'"{task.title}" 과제를 미완료로 변경했습니다.'
        else:
            task.status = 'COMPLETED'
            task.progress = 100
            message = f'"{task.title}" 과제를 완료했습니다!'
        
        task.save()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'new_status': task.get_status_display(),
            'new_status_class': task.get_status_badge_class()
        })

class TaskQuickAddView(LoginRequiredMixin, CreateView):
    """빠른 과제 추가 뷰 (AJAX)"""
    model = Task
    form_class = TaskQuickAddForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        task = form.save()
        
        return JsonResponse({
            'success': True,
            'message': f'"{task.title}" 과제가 추가되었습니다.',
            'task_id': str(task.id)
        })
    
    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })

class StudySessionListView(LoginRequiredMixin, ListView):
    """학습 세션 목록 뷰"""
    model = StudySession
    template_name = 'planner/study_session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20
    
    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user).select_related('task', 'subject')

class StudySessionCreateView(LoginRequiredMixin, CreateView):
    """학습 세션 생성 뷰"""
    model = StudySession
    form_class = StudySessionForm
    template_name = 'planner/study_session_create.html'
    success_url = reverse_lazy('planner:study_session_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '학습 세션이 기록되었습니다.')
        return super().form_valid(form)

class GoalListView(LoginRequiredMixin, ListView):
    """목표 목록 뷰"""
    model = Goal
    template_name = 'planner/goal_list.html'
    context_object_name = 'goals'
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 각 목표의 진행률 계산
        for goal in context['goals']:
            goal.progress_percentage = goal.get_progress_percentage()
        
        return context

class GoalCreateView(LoginRequiredMixin, CreateView):
    """목표 생성 뷰"""
    model = Goal
    form_class = GoalForm
    template_name = 'planner/goal_create.html'
    success_url = reverse_lazy('planner:goal_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'"{form.instance.title}" 목표가 설정되었습니다.')
        return super().form_valid(form)
