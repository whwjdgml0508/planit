from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.PlannerView.as_view(), name='index'),
    
    # 과제 관련 URL
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<uuid:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<uuid:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<uuid:pk>/toggle/', views.TaskToggleView.as_view(), name='task_toggle'),
    
    # 학습 세션 관련 URL
    path('sessions/', views.StudySessionListView.as_view(), name='study_session_list'),
    
    # 목표 관련 URL
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goals/create/', views.GoalCreateView.as_view(), name='goal_create'),
    path('goals/<uuid:pk>/edit/', views.GoalUpdateView.as_view(), name='goal_edit'),
    path('goals/<uuid:pk>/delete/', views.GoalDeleteView.as_view(), name='goal_delete'),
    
    # 일일 플래너
    path('daily/', views.DailyPlannerView.as_view(), name='daily_planner'),
    
    # AJAX 뷰들
    path('ajax/add-todo/', views.add_todo_item, name='add_todo_item'),
    path('ajax/toggle-todo/<uuid:todo_id>/', views.toggle_todo_item, name='toggle_todo_item'),
    path('ajax/delete-todo/<uuid:todo_id>/', views.delete_todo_item, name='delete_todo_item'),
    path('ajax/add-time-block/', views.add_time_block, name='add_time_block'),
    path('ajax/remove-time-block/', views.remove_time_block, name='remove_time_block'),
    path('ajax/update-daily-goal/', views.update_daily_goal, name='update_daily_goal'),
    path('ajax/update-target-hours/', views.update_target_hours, name='update_target_hours'),
    path('ajax/update-goal-progress/<uuid:goal_id>/', views.update_goal_progress, name='update_goal_progress'),
    path('ajax/update-weekly-study-goal/', views.update_weekly_study_goal, name='update_weekly_study_goal'),
    
    # 하위 목표 (SubGoal) AJAX API
    path('ajax/goals/<uuid:goal_id>/subgoals/', views.get_subgoals, name='get_subgoals'),
    path('ajax/goals/<uuid:goal_id>/subgoals/add/', views.add_subgoal, name='add_subgoal'),
    path('ajax/subgoals/<uuid:subgoal_id>/toggle/', views.toggle_subgoal, name='toggle_subgoal'),
    path('ajax/subgoals/<uuid:subgoal_id>/delete/', views.delete_subgoal, name='delete_subgoal'),
    path('ajax/subgoals/<uuid:subgoal_id>/update/', views.update_subgoal, name='update_subgoal'),
]
