from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # 시간표 메인
    path('', views.TimetableView.as_view(), name='index'),
    
    # 과목 관리
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/create/', views.SubjectOnlyCreateView.as_view(), name='subject_create'),
    path('subject/create-with-timetable/', views.SubjectCreateView.as_view(), name='subject_create_with_timetable'),
    path('subject/create-improved/', views.ImprovedSubjectCreateView.as_view(), name='subject_create_improved'),
    path('subject/<uuid:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/<uuid:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subject/<uuid:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    
    # 시간표 관리
    path('manage/', views.TimetableManageView.as_view(), name='timetable_manage'),
    path('ajax/add-to-timetable/', views.add_to_timetable, name='add_to_timetable'),
    path('ajax/remove-from-timetable/', views.remove_from_timetable, name='remove_from_timetable'),
    path('ajax/get-timetable-data/', views.get_timetable_data, name='get_timetable_data'),
    
    # 기존 기능
    path('subject/<uuid:subject_id>/timeslot/add/', views.TimeSlotCreateView.as_view(), name='timeslot_add'),
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semester/create/', views.SemesterCreateView.as_view(), name='semester_create'),
]