from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Task, StudySession, Goal, SubGoal, DailyPlanner, TimeBlock, TodoItem
from .forms import TaskForm, StudySessionForm, GoalForm, TaskFilterForm

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
        
        # 이번 주 과제 (마감일이 이번 주이거나, 마감일 미설정 과제 중 이번 주 생성된 과제)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_tasks = Task.objects.filter(
            user=user,
            status__in=['TODO', 'IN_PROGRESS']
        ).filter(
            Q(due_date__date__range=[week_start, week_end]) |  # 마감일이 이번 주
            Q(due_date__isnull=True, created_at__date__range=[week_start, week_end])  # 마감일 미설정 + 이번 주 생성
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
        
        # 이번 주 총 학습시간 (StudySession)
        # duration_minutes가 NULL인 경우를 대비해 직접 계산
        session_study_minutes = 0
        for session in week_sessions:
            if session.duration_minutes:
                session_study_minutes += session.duration_minutes
            elif session.start_time and session.end_time:
                # duration_minutes가 없으면 직접 계산
                duration = session.end_time - session.start_time
                session_study_minutes += int(duration.total_seconds() / 60)
        
        # 이번 주 총 학습시간 (TimeBlock - 일일 플래너)
        timeblock_study_minutes = TimeBlock.objects.filter(
            daily_planner__user=user,
            daily_planner__date__range=[week_start, week_end],
            block_type='STUDY'
        ).count() * 10  # 각 블록은 10분
        
        # 총 학습시간 합산
        total_study_minutes = session_study_minutes + timeblock_study_minutes
        
        # 활성 목표 (달성되지 않은 모든 목표 표시)
        active_goals = Goal.objects.filter(
            user=user,
            is_achieved=False
        ).order_by('end_date')
        
        # 통계
        task_stats = {
            'total': Task.objects.filter(user=user).count(),
            'completed': Task.objects.filter(user=user, status='COMPLETED').count(),
            'in_progress': Task.objects.filter(user=user, status='IN_PROGRESS').count(),
            'overdue': overdue_tasks.count(),
        }
        
        # 완료율 계산
        completion_rate = 0
        if task_stats['total'] > 0:
            completion_rate = round((task_stats['completed'] / task_stats['total']) * 100, 1)
        
        # 3일 이내 마감 과제
        upcoming_deadline = Task.objects.filter(
            user=user,
            due_date__date__range=[today, today + timedelta(days=3)],
            status__in=['TODO', 'IN_PROGRESS']
        ).order_by('due_date')
        
        # 일일 학습시간 (최근 7일)
        daily_study_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            
            # StudySession 학습시간
            day_sessions = StudySession.objects.filter(
                user=user,
                start_time__date=day,
                end_time__isnull=False
            )
            session_minutes = sum(
                s.duration_minutes if s.duration_minutes else 
                int((s.end_time - s.start_time).total_seconds() / 60)
                for s in day_sessions
            )
            
            # TimeBlock 학습시간 (일일 플래너)
            timeblock_minutes = TimeBlock.objects.filter(
                daily_planner__user=user,
                daily_planner__date=day,
                block_type='STUDY'
            ).count() * 10  # 각 블록은 10분
            
            # 총 학습시간
            day_minutes = session_minutes + timeblock_minutes
            
            daily_study_data.append({
                'date': day.strftime('%m/%d'),
                'day_name': ['월', '화', '수', '목', '금', '토', '일'][day.weekday()],
                'minutes': day_minutes,
                'hours': round(day_minutes / 60, 1)
            })
        
        # 오늘 학습시간
        today_study_minutes = daily_study_data[-1]['minutes'] if daily_study_data else 0
        
        context.update({
            'today_tasks': today_tasks,
            'week_tasks': week_tasks,
            'overdue_tasks': overdue_tasks,
            'recent_completed': recent_completed,
            'week_sessions': week_sessions,
            'total_study_hours': float(total_study_minutes) / 60.0,
            'today_study_hours': float(today_study_minutes) / 60.0,
            'active_goals': active_goals,
            'task_stats': task_stats,
            'completion_rate': completion_rate,
            'upcoming_deadline': upcoming_deadline,
            'daily_study_data': daily_study_data,
            'weekly_study_goal': getattr(user, 'weekly_study_goal', 40),
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

class StudySessionListView(LoginRequiredMixin, TemplateView):
    """학습 세션 목록 뷰 - 일일 플래너로 리다이렉트"""
    
    def get(self, request, *args, **kwargs):
        return redirect('planner:daily_planner')

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

class GoalCreateView(LoginRequiredMixin, CreateView):
    """목표 생성 뷰"""
    model = Goal
    form_class = GoalForm
    template_name = 'planner/goal_create.html'
    success_url = reverse_lazy('planner:goal_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # 사용자 정의 목표인 경우 하위 목표 처리
        if form.instance.goal_type == 'CUSTOM':
            import json
            subgoals_data = self.request.POST.get('subgoals_data', '[]')
            try:
                subgoals_titles = json.loads(subgoals_data)
                for order, title in enumerate(subgoals_titles):
                    if title.strip():
                        SubGoal.objects.create(
                            goal=form.instance,
                            title=title.strip(),
                            order=order
                        )
                if subgoals_titles:
                    messages.success(self.request, f'"{form.instance.title}" 목표가 {len(subgoals_titles)}개의 세부 목표와 함께 설정되었습니다.')
                else:
                    messages.success(self.request, f'"{form.instance.title}" 목표가 설정되었습니다.')
            except json.JSONDecodeError:
                messages.success(self.request, f'"{form.instance.title}" 목표가 설정되었습니다.')
        else:
            messages.success(self.request, f'"{form.instance.title}" 목표가 설정되었습니다.')
        
        return response

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    """목표 수정 뷰"""
    model = Goal
    form_class = GoalForm
    template_name = 'planner/goal_edit.html'
    success_url = reverse_lazy('planner:goal_list')
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.title}" 목표가 수정되었습니다.')
        return super().form_valid(form)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    """목표 삭제 뷰"""
    model = Goal
    template_name = 'planner/goal_delete.html'
    success_url = reverse_lazy('planner:goal_list')
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        goal = self.get_object()
        goal_title = goal.title
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'"{goal_title}" 목표가 삭제되었습니다.')
        return result


class DailyPlannerView(LoginRequiredMixin, TemplateView):
    """일일 플래너 뷰"""
    template_name = 'planner/daily_planner.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 날짜 파라미터 처리
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = timezone.now().date()
        else:
            target_date = timezone.now().date()
        
        # 해당 날짜의 플래너 가져오기 또는 생성
        daily_planner, created = DailyPlanner.objects.get_or_create(
            user=user,
            date=target_date,
            defaults={'target_study_hours': 8.0}
        )
        
        # 시간 블록 데이터 생성 (6시~23시, 10분 단위)
        time_blocks = {}
        for hour in range(6, 24):
            time_blocks[hour] = {}
            for minute_block in range(6):  # 0-5 (00, 10, 20, 30, 40, 50분)
                try:
                    block = TimeBlock.objects.get(
                        daily_planner=daily_planner,
                        hour=hour,
                        minute_block=minute_block
                    )
                    time_blocks[hour][minute_block] = block
                except TimeBlock.DoesNotExist:
                    time_blocks[hour][minute_block] = None
        
        # 할 일 목록
        todo_items = daily_planner.todo_items.all()
        
        # 과목 목록
        from timetable.models import Subject
        subjects = Subject.objects.filter(user=user)
        
        # 총 학습시간 계산
        total_study_minutes = TimeBlock.objects.filter(
            daily_planner=daily_planner,
            block_type='STUDY'
        ).count() * 10
        
        # 통계 데이터 계산
        completed_todos = todo_items.filter(is_completed=True).count()
        total_todos = todo_items.count()
        
        # 이번 주 과제 (마감일 기준)
        week_start = target_date - timedelta(days=target_date.weekday())
        week_end = week_start + timedelta(days=6)
        
        overdue_tasks = Task.objects.filter(
            user=user,
            due_date__lt=timezone.now(),
            status__in=['TODO', 'IN_PROGRESS']
        ).count()
        
        # 통계 데이터
        actual_hours = float(total_study_minutes) / 60.0
        target_hours = float(daily_planner.target_study_hours)
        achievement_rate = min(100, int((actual_hours / target_hours * 100) if target_hours > 0 else 0))
        
        stats = {
            'completed_todos': completed_todos,
            'total_todos': total_todos,
            'study_hours': actual_hours,
            'target_hours': target_hours,
            'achievement_rate': achievement_rate,
            'overdue_tasks': overdue_tasks,
        }
        
        context.update({
            'daily_planner': daily_planner,
            'target_date': target_date,
            'selected_date': target_date,  # 템플릿에서 사용
            'today': timezone.now().date(),
            'time_blocks': time_blocks,
            'todo_items': todo_items,
            'subjects': subjects,
            'total_study_hours': float(total_study_minutes) / 60.0,
            'hours_range': range(6, 24),
            'minute_blocks_range': range(6),
            'stats': stats,
        })
        
        return context


@login_required
def add_todo_item(request):
    """할 일 추가 (AJAX)"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        title = request.POST.get('title', '').strip()
        priority = request.POST.get('priority', 'MEDIUM')
        
        if not title:
            return JsonResponse({'success': False, 'error': '할 일을 입력해주세요.'})
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = timezone.now().date()
        
        # 일일 플래너 가져오기 또는 생성
        daily_planner, created = DailyPlanner.objects.get_or_create(
            user=request.user,
            date=date
        )
        
        # 할 일 추가
        todo_item = TodoItem.objects.create(
            daily_planner=daily_planner,
            title=title,
            priority=priority,
            order=TodoItem.objects.filter(daily_planner=daily_planner).count()
        )
        
        return JsonResponse({
            'success': True,
            'todo_id': str(todo_item.id),
            'title': todo_item.title,
            'priority': todo_item.get_priority_display()
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def toggle_todo_item(request, todo_id):
    """할 일 완료 토글 (AJAX)"""
    if request.method == 'POST':
        todo_item = get_object_or_404(TodoItem, id=todo_id, daily_planner__user=request.user)
        
        todo_item.is_completed = not todo_item.is_completed
        todo_item.save()
        
        return JsonResponse({
            'success': True,
            'is_completed': todo_item.is_completed,
            'completed_at': todo_item.completed_at.strftime('%H:%M') if todo_item.completed_at else None
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def delete_todo_item(request, todo_id):
    """할 일 삭제 (AJAX)"""
    if request.method == 'POST':
        todo_item = get_object_or_404(TodoItem, id=todo_id, daily_planner__user=request.user)
        todo_item.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def add_time_block(request):
    """시간 블록 추가/수정 (AJAX)"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        hour = int(request.POST.get('hour'))
        minute_block = int(request.POST.get('minute_block'))
        block_type = request.POST.get('block_type', 'STUDY')
        subject_id = request.POST.get('subject_id')
        color = request.POST.get('color', '#3498db')
        memo = request.POST.get('memo', '')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = timezone.now().date()
        
        # 일일 플래너 가져오기 또는 생성
        daily_planner, created = DailyPlanner.objects.get_or_create(
            user=request.user,
            date=date
        )
        
        # 시간 블록 생성 또는 업데이트
        time_block, created = TimeBlock.objects.update_or_create(
            daily_planner=daily_planner,
            hour=hour,
            minute_block=minute_block,
            defaults={
                'block_type': block_type,
                'subject_id': subject_id if subject_id else None,
                'color': color,
                'memo': memo
            }
        )
        
        subject_name = time_block.subject.name if time_block.subject else ''
        
        return JsonResponse({
            'success': True,
            'block_id': str(time_block.id),
            'subject_name': subject_name,
            'color': time_block.color,
            'memo': time_block.memo
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def remove_time_block(request):
    """시간 블록 제거 (AJAX)"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        hour = int(request.POST.get('hour'))
        minute_block = int(request.POST.get('minute_block'))
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = timezone.now().date()
        
        # 시간 블록 찾아서 삭제
        try:
            time_block = TimeBlock.objects.get(
                daily_planner__user=request.user,
                daily_planner__date=date,
                hour=hour,
                minute_block=minute_block
            )
            time_block.delete()
            return JsonResponse({'success': True})
        except TimeBlock.DoesNotExist:
            return JsonResponse({'success': False, 'error': '시간 블록을 찾을 수 없습니다.'})
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def update_daily_goal(request):
    """일일 목표 업데이트 (AJAX)"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        goal = request.POST.get('goal', '')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = timezone.now().date()
        
        # 일일 플래너 업데이트
        daily_planner, created = DailyPlanner.objects.get_or_create(
            user=request.user,
            date=date,
            defaults={'daily_goal': goal}
        )
        
        if not created:
            daily_planner.daily_goal = goal
            daily_planner.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def update_goal_progress(request, goal_id):
    """목표 진행률 업데이트 (AJAX)"""
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        
        try:
            progress = int(request.POST.get('progress', 0))
            progress = max(0, min(100, progress))  # 0-100 범위로 제한
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': '유효하지 않은 진행률입니다.'})
        
        goal.progress = progress
        goal.save()
        
        return JsonResponse({
            'success': True,
            'progress': goal.progress,
            'is_achieved': goal.is_achieved,
            'message': f'진행률이 {goal.progress}%로 업데이트되었습니다.' if goal.progress < 100 else '🎉 목표를 달성했습니다!'
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def update_target_hours(request):
    """목표 학습시간 업데이트 (AJAX)"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        target_hours = request.POST.get('target_hours')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            date = timezone.now().date()
        
        try:
            target_hours = float(target_hours)
            if target_hours < 0.1 or target_hours > 24.0:
                return JsonResponse({'success': False, 'error': '목표 시간은 0.1시간에서 24시간 사이여야 합니다.'})
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': '유효하지 않은 시간입니다.'})
        
        # 일일 플래너 업데이트
        daily_planner, created = DailyPlanner.objects.get_or_create(
            user=request.user,
            date=date,
            defaults={'target_study_hours': target_hours}
        )
        
        if not created:
            daily_planner.target_study_hours = target_hours
            daily_planner.save()
        
        return JsonResponse({
            'success': True,
            'target_hours': float(daily_planner.target_study_hours),
            'message': f'목표 학습시간이 {target_hours}시간으로 설정되었습니다.'
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


# ==================== 하위 목표 (SubGoal) AJAX API ====================

@login_required
def add_subgoal(request, goal_id):
    """하위 목표 추가 (AJAX)"""
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id, user=request.user)
        
        # 사용자 정의 목표만 하위 목표 추가 가능
        if goal.goal_type != 'CUSTOM':
            return JsonResponse({'success': False, 'error': '사용자 정의 목표에만 하위 목표를 추가할 수 있습니다.'})
        
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not title:
            return JsonResponse({'success': False, 'error': '하위 목표를 입력해주세요.'})
        
        # 순서 계산
        max_order = goal.subgoals.count()
        
        subgoal = SubGoal.objects.create(
            goal=goal,
            title=title,
            description=description,
            order=max_order
        )
        
        return JsonResponse({
            'success': True,
            'subgoal_id': str(subgoal.id),
            'title': subgoal.title,
            'description': subgoal.description,
            'is_completed': subgoal.is_completed,
            'goal_progress': goal.progress
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def toggle_subgoal(request, subgoal_id):
    """하위 목표 완료 토글 (AJAX)"""
    if request.method == 'POST':
        subgoal = get_object_or_404(SubGoal, id=subgoal_id, goal__user=request.user)
        
        subgoal.is_completed = not subgoal.is_completed
        subgoal.save()  # save()에서 상위 목표 진행률 자동 업데이트
        
        goal = subgoal.goal
        
        return JsonResponse({
            'success': True,
            'is_completed': subgoal.is_completed,
            'completed_at': subgoal.completed_at.strftime('%Y-%m-%d %H:%M') if subgoal.completed_at else None,
            'goal_progress': goal.progress,
            'goal_is_achieved': goal.is_achieved,
            'message': '🎉 목표를 달성했습니다!' if goal.is_achieved else None
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def delete_subgoal(request, subgoal_id):
    """하위 목표 삭제 (AJAX)"""
    if request.method == 'POST':
        subgoal = get_object_or_404(SubGoal, id=subgoal_id, goal__user=request.user)
        goal = subgoal.goal
        
        subgoal.delete()
        
        # 삭제 후 상위 목표 진행률 재계산
        goal.update_progress_from_subgoals()
        
        return JsonResponse({
            'success': True,
            'goal_progress': goal.progress,
            'goal_is_achieved': goal.is_achieved
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def update_subgoal(request, subgoal_id):
    """하위 목표 수정 (AJAX)"""
    if request.method == 'POST':
        subgoal = get_object_or_404(SubGoal, id=subgoal_id, goal__user=request.user)
        
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not title:
            return JsonResponse({'success': False, 'error': '하위 목표를 입력해주세요.'})
        
        subgoal.title = title
        subgoal.description = description
        subgoal.save()
        
        return JsonResponse({
            'success': True,
            'title': subgoal.title,
            'description': subgoal.description
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
def get_subgoals(request, goal_id):
    """하위 목표 목록 조회 (AJAX)"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    subgoals = goal.subgoals.all()
    subgoals_data = [{
        'id': str(sg.id),
        'title': sg.title,
        'description': sg.description,
        'is_completed': sg.is_completed,
        'completed_at': sg.completed_at.strftime('%Y-%m-%d %H:%M') if sg.completed_at else None,
        'order': sg.order
    } for sg in subgoals]
    
    return JsonResponse({
        'success': True,
        'subgoals': subgoals_data,
        'goal_progress': goal.progress,
        'goal_is_achieved': goal.is_achieved
    })


@login_required
def update_weekly_study_goal(request):
    """주간 학습 목표 업데이트 (AJAX)"""
    if request.method == 'POST':
        try:
            weekly_goal = int(request.POST.get('weekly_goal', 40))
            if weekly_goal < 1 or weekly_goal > 168:
                return JsonResponse({'success': False, 'error': '주간 목표는 1시간에서 168시간 사이여야 합니다.'})
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': '유효하지 않은 시간입니다.'})
        
        user = request.user
        try:
            user.weekly_study_goal = weekly_goal
            user.save(update_fields=['weekly_study_goal'])
        except Exception:
            return JsonResponse({'success': False, 'error': '아직 이 기능을 사용할 수 없습니다. 서버 업데이트가 필요합니다.'})
        
        return JsonResponse({
            'success': True,
            'weekly_goal': weekly_goal,
            'message': f'주간 학습 목표가 {weekly_goal}시간으로 설정되었습니다.'
        })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})
