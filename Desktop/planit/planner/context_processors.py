from django.utils import timezone
from datetime import timedelta

def deadline_notifications(request):
    """마감 임박 과제 및 지난 과제 수를 제공하는 context processor"""
    context = {
        'urgent_tasks_count': 0,
        'overdue_tasks_count': 0,
    }
    
    if request.user.is_authenticated:
        from .models import Task
        today = timezone.now().date()
        
        # 3일 이내 마감 과제 수
        urgent_count = Task.objects.filter(
            user=request.user,
            due_date__date__range=[today, today + timedelta(days=3)],
            status__in=['TODO', 'IN_PROGRESS']
        ).count()
        
        # 마감 지난 과제 수
        overdue_count = Task.objects.filter(
            user=request.user,
            due_date__lt=timezone.now(),
            status__in=['TODO', 'IN_PROGRESS']
        ).count()
        
        context['urgent_tasks_count'] = urgent_count
        context['overdue_tasks_count'] = overdue_count
        context['total_pending_tasks'] = urgent_count + overdue_count
    
    return context
