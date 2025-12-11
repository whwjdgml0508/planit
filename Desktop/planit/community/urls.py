from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.CommunityView.as_view(), name='index'),
    
    # 게시글 관련 URL
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<uuid:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<uuid:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<uuid:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<uuid:pk>/like/', views.PostLikeToggleView.as_view(), name='post_like_toggle'),
    
    # 카테고리 관련 URL
    path('category/<slug:slug>/', views.CategoryPostListView.as_view(), name='category_posts'),
    
    # 첨부파일 관련 URL
    path('attachment/<uuid:pk>/download/', views.AttachmentDownloadView.as_view(), name='attachment_download'),
    
    # 신고 관련 URL
    path('report/', views.ReportCreateView.as_view(), name='report_create'),
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<uuid:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<uuid:pk>/update-status/', views.ReportUpdateStatusView.as_view(), name='report_update_status'),
    
    # 댓글 관련 URL
    path('comment/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
