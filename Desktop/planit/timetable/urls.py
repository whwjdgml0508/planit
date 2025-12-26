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
    
    # 파일 관리
    path('subject/<uuid:subject_id>/file/upload/', views.SubjectFileUploadView.as_view(), name='subject_file_upload'),
    path('file/<uuid:pk>/delete/', views.SubjectFileDeleteView.as_view(), name='subject_file_delete'),
    path('file/<uuid:pk>/download/', views.download_subject_file, name='subject_file_download'),
    
    # 시간표 관리
    path('manage/', views.TimetableManageView.as_view(), name='timetable_manage'),
    path('ajax/add-to-timetable/', views.add_to_timetable, name='add_to_timetable'),
    path('ajax/remove-from-timetable/', views.remove_from_timetable, name='remove_from_timetable'),
    path('ajax/get-timetable-data/', views.get_timetable_data, name='get_timetable_data'),
    
    # 기존 기능
    path('subject/<uuid:subject_id>/timeslot/add/', views.TimeSlotCreateView.as_view(), name='timeslot_add'),
    
    # 학기 관리
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semester/create/', views.SemesterCreateView.as_view(), name='semester_create'),
    path('semester/<uuid:pk>/edit/', views.SemesterUpdateView.as_view(), name='semester_edit'),
    path('semester/<uuid:pk>/set-current/', views.set_current_semester, name='semester_set_current'),
    path('semester/<uuid:pk>/delete/', views.delete_semester, name='semester_delete'),
]