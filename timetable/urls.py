from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.TimetableView.as_view(), name='index'),
    path('subject/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subject/<uuid:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/<uuid:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subject/<uuid:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('subject/<uuid:subject_id>/timeslot/add/', views.TimeSlotCreateView.as_view(), name='timeslot_add'),
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semester/create/', views.SemesterCreateView.as_view(), name='semester_create'),
]
