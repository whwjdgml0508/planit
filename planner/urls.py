from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.PlannerView.as_view(), name='index'),
    
    # 과제 관련 URL
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/quick-add/', views.TaskQuickAddView.as_view(), name='task_quick_add'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<uuid:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<uuid:pk>/toggle/', views.TaskToggleView.as_view(), name='task_toggle'),
    
    # 학습 세션 관련 URL
    path('sessions/', views.StudySessionListView.as_view(), name='study_session_list'),
    path('sessions/create/', views.StudySessionCreateView.as_view(), name='study_session_create'),
    
    # 목표 관련 URL
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goals/create/', views.GoalCreateView.as_view(), name='goal_create'),
]
