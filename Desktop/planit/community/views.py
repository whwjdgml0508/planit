from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Prefetch
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Category, Post, Comment, Attachment, Report
from .forms import PostForm, CommentForm, ReplyForm, PostSearchForm, ReportForm, AttachmentForm

class CommunityView(LoginRequiredMixin, TemplateView):
    """커뮤니티 메인 뷰"""
    template_name = 'community/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 접근 가능한 카테고리 필터링
        categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            categories = categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        
        # 각 카테고리별 게시글 수 추가
        categories = categories.annotate(
            post_count=Count('posts', filter=Q(posts__is_active=True))
        ).order_by('order', 'name')
        
        # 최근 게시글
        recent_posts = Post.objects.filter(
            is_active=True,
            category__in=categories
        ).select_related('author', 'category').order_by('-created_at')[:10]
        
        # 인기 게시글 (좋아요 많은 순)
        popular_posts = Post.objects.filter(
            is_active=True,
            category__in=categories,
            created_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).annotate(
            like_count=Count('likes')
        ).order_by('-like_count', '-views')[:5]
        
        # 공지사항
        notices = Post.objects.filter(
            is_active=True,
            post_type='NOTICE',
            category__in=categories
        ).order_by('-is_pinned', '-created_at')[:5]
        
        context.update({
            'categories': categories,
            'recent_posts': recent_posts,
            'popular_posts': popular_posts,
            'notices': notices,
        })
        return context

class PostListView(LoginRequiredMixin, ListView):
    """게시글 목록 뷰"""
    model = Post
    template_name = 'community/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        
        # 접근 가능한 카테고리 필터링
        accessible_categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            accessible_categories = accessible_categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        
        queryset = Post.objects.filter(
            is_active=True,
            category__in=accessible_categories
        ).select_related('author', 'category', 'subject').prefetch_related('likes')
        
        # 작성자 필터링 (프로필에서 넘어온 경우)
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # 검색 처리
        search_form = PostSearchForm(self.request.GET, user=user)
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            search_type = search_form.cleaned_data.get('search_type')
            category = search_form.cleaned_data.get('category')
            post_type = search_form.cleaned_data.get('post_type')
            
            if query:
                if search_type == 'title':
                    queryset = queryset.filter(title__icontains=query)
                elif search_type == 'content':
                    queryset = queryset.filter(content__icontains=query)
                elif search_type == 'author':
                    queryset = queryset.filter(author__username__icontains=query)
                elif search_type == 'tags':
                    queryset = queryset.filter(tags__icontains=query)
                else:  # all
                    queryset = queryset.filter(
                        Q(title__icontains=query) |
                        Q(content__icontains=query) |
                        Q(author__username__icontains=query) |
                        Q(tags__icontains=query)
                    )
            
            if category:
                queryset = queryset.filter(category=category)
            
            if post_type:
                queryset = queryset.filter(post_type=post_type)
        
        return queryset.order_by('-is_pinned', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PostSearchForm(self.request.GET, user=self.request.user)
        
        # 카테고리 목록 추가
        user = self.request.user
        categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            categories = categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        context['categories'] = categories.order_by('order', 'name')
        
        # 작성자 필터링 정보 추가
        author_id = self.request.GET.get('author')
        if author_id:
            from accounts.models import User
            try:
                author = User.objects.get(id=author_id)
                context['filtered_author'] = author
            except User.DoesNotExist:
                pass
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """게시글 생성 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'community/post_create.html'
    success_url = reverse_lazy('community:post_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 사용자가 접근 가능한 카테고리 목록 추가
        categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            categories = categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        
        context['categories'] = categories.order_by('order', 'name')
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # 첨부파일 처리
        files = self.request.FILES.getlist('attachments')
        for file in files:
            # 파일 유형 결정
            ext = file.name.split('.')[-1].lower() if '.' in file.name else ''
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']:
                file_type = 'IMAGE'
            elif ext in ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'hwp']:
                file_type = 'DOCUMENT'
            elif ext in ['zip', 'rar', '7z', 'tar', 'gz']:
                file_type = 'ARCHIVE'
            else:
                file_type = 'OTHER'
            
            attachment = Attachment(
                post=self.object,
                uploader=self.request.user,
                file=file,
                original_name=file.name,
                file_size=file.size,
                file_type=file_type
            )
            attachment.save()
        
        messages.success(self.request, f'"{self.object.title}" 게시글이 작성되었습니다.')
        return response

class PostDetailView(LoginRequiredMixin, DetailView):
    """게시글 상세 뷰"""
    model = Post
    template_name = 'community/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        user = self.request.user
        
        # 접근 가능한 카테고리의 게시글만
        accessible_categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            accessible_categories = accessible_categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        
        return Post.objects.filter(
            is_active=True,
            category__in=accessible_categories
        ).select_related('author', 'category', 'subject').prefetch_related(
            'attachments',
            'likes',
            Prefetch('comments', queryset=Comment.objects.filter(
                is_active=True, parent__isnull=True
            ).select_related('author').prefetch_related(
                Prefetch('replies', queryset=Comment.objects.filter(
                    is_active=True
                ).select_related('author'))
            ))
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # 조회수 증가
        post.increment_views()
        
        # 댓글 폼
        context['comment_form'] = CommentForm()
        context['reply_form'] = ReplyForm()
        
        # 사용자가 좋아요 했는지 확인
        context['user_liked'] = post.is_liked_by(self.request.user)
        
        # 같은 카테고리의 관련 게시글 (최신순 5개, 현재 글 제외)
        related_posts = Post.objects.filter(
            category=post.category,
            is_active=True
        ).exclude(id=post.id).select_related('author').order_by('-created_at')[:5]
        context['related_posts'] = related_posts
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # 댓글 작성 처리
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = self.object
                comment.author = request.user
                comment.save()
                messages.success(request, '댓글이 작성되었습니다.')
                return redirect(self.object.get_absolute_url())
        
        # 대댓글 작성 처리
        elif 'reply_submit' in request.POST:
            reply_form = ReplyForm(request.POST)
            parent_id = request.POST.get('parent_id')
            if reply_form.is_valid() and parent_id:
                reply = reply_form.save(commit=False)
                reply.post = self.object
                reply.author = request.user
                reply.parent_id = parent_id
                reply.save()
                messages.success(request, '답글이 작성되었습니다.')
                return redirect(self.object.get_absolute_url())
        
        return self.get(request, *args, **kwargs)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    """게시글 수정 뷰"""
    model = Post
    form_class = PostForm
    template_name = 'community/post_edit.html'
    
    def get_queryset(self):
        # 작성자만 수정 가능
        return Post.objects.filter(author=self.request.user, is_active=True)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 사용자가 접근 가능한 카테고리 목록 추가
        categories = Category.objects.filter(is_active=True)
        if not user.is_staff:
            categories = categories.filter(
                Q(department_restricted=False) |
                Q(allowed_departments__icontains=user.department)
            )
        
        context['categories'] = categories.order_by('order', 'name')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # 새 첨부파일 처리
        files = self.request.FILES.getlist('new_attachments')
        for file in files:
            # 파일 유형 결정
            ext = file.name.split('.')[-1].lower() if '.' in file.name else ''
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']:
                file_type = 'IMAGE'
            elif ext in ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'hwp']:
                file_type = 'DOCUMENT'
            elif ext in ['zip', 'rar', '7z', 'tar', 'gz']:
                file_type = 'ARCHIVE'
            else:
                file_type = 'OTHER'
            
            attachment = Attachment(
                post=self.object,
                uploader=self.request.user,
                file=file,
                original_name=file.name,
                file_size=file.size,
                file_type=file_type
            )
            attachment.save()
        
        messages.success(self.request, f'"{self.object.title}" 게시글이 수정되었습니다.')
        return response

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """게시글 삭제 뷰"""
    model = Post
    template_name = 'community/post_delete.html'
    success_url = reverse_lazy('community:post_list')
    
    def get_queryset(self):
        # 작성자만 삭제 가능
        return Post.objects.filter(author=self.request.user, is_active=True)
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post_title = post.title
        # 실제 삭제 대신 비활성화
        post.is_active = False
        post.save()
        messages.success(request, f'"{post_title}" 게시글이 삭제되었습니다.')
        return redirect(self.success_url)

class CategoryPostListView(LoginRequiredMixin, ListView):
    """카테고리별 게시글 목록 뷰"""
    model = Post
    template_name = 'community/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        
        # 접근 권한 확인
        user = self.request.user
        if self.category.department_restricted and not user.is_staff:
            if user.department not in self.category.allowed_departments:
                messages.error(self.request, '이 카테고리에 접근할 권한이 없습니다.')
                return Post.objects.none()
        
        return Post.objects.filter(
            category=self.category,
            is_active=True
        ).select_related('author', 'subject').prefetch_related('likes').order_by('-is_pinned', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class PostLikeToggleView(LoginRequiredMixin, TemplateView):
    """게시글 좋아요 토글 뷰 (AJAX)"""
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = get_object_or_404(Post, id=post_id, is_active=True)
        
        if post.is_liked_by(request.user):
            post.likes.remove(request.user)
            liked = False
            message = '좋아요를 취소했습니다.'
        else:
            post.likes.add(request.user)
            liked = True
            message = '좋아요를 눌렀습니다.'
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': post.get_like_count(),
            'message': message
        })

class AttachmentDownloadView(LoginRequiredMixin, TemplateView):
    """첨부파일 다운로드 뷰"""
    
    def get(self, request, *args, **kwargs):
        import mimetypes
        from urllib.parse import quote
        
        attachment_id = kwargs.get('pk')
        attachment = get_object_or_404(Attachment, id=attachment_id)
        
        # 다운로드 수 증가
        attachment.increment_download()
        
        # 파일 열기
        attachment.file.open('rb')
        
        # MIME 타입 결정
        content_type, _ = mimetypes.guess_type(attachment.original_name)
        if not content_type:
            content_type = 'application/octet-stream'
        
        # 파일 응답 생성
        response = HttpResponse(attachment.file.read(), content_type=content_type)
        
        # 파일 닫기
        attachment.file.close()
        
        # 한글 파일명 인코딩 처리
        encoded_filename = quote(attachment.original_name)
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
        response['Content-Length'] = attachment.file_size
        
        return response

class ReportCreateView(LoginRequiredMixin, View):
    """신고 생성 뷰 (AJAX)"""
    
    def post(self, request, *args, **kwargs):
        try:
            # POST 데이터에서 정보 추출
            post_id = request.POST.get('post_id')
            comment_id = request.POST.get('comment_id')
            report_type = request.POST.get('report_type')
            reason = request.POST.get('reason')
            
            # 필수 필드 검증
            if not report_type or not reason:
                return JsonResponse({
                    'success': False,
                    'message': '신고 유형과 사유를 모두 입력해주세요.'
                }, status=400)
            
            # 신고 대상 검증
            if not post_id and not comment_id:
                return JsonResponse({
                    'success': False,
                    'message': '신고 대상이 지정되지 않았습니다.'
                }, status=400)
            
            # 신고 생성
            report = Report(
                reporter=request.user,
                report_type=report_type,
                reason=reason
            )
            
            if post_id:
                post = get_object_or_404(Post, id=post_id)
                report.post = post
            elif comment_id:
                comment = get_object_or_404(Comment, id=comment_id)
                report.comment = comment
            
            report.save()
            
            return JsonResponse({
                'success': True,
                'message': '신고가 접수되었습니다. 검토 후 조치하겠습니다.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'신고 접수 중 오류가 발생했습니다: {str(e)}'
            }, status=500)

class CommentDeleteView(LoginRequiredMixin, View):
    """댓글 삭제 뷰"""
    
    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('pk')
        comment = get_object_or_404(Comment, id=comment_id)
        
        # 작성자만 삭제 가능
        if comment.author != request.user:
            return JsonResponse({'success': False, 'message': '권한이 없습니다.'}, status=403)
        
        post = comment.post
        comment.delete()
        
        messages.success(request, '댓글이 삭제되었습니다.')
        return JsonResponse({'success': True, 'redirect_url': post.get_absolute_url()})

class ReportListView(UserPassesTestMixin, ListView):
    """관리자용 신고 목록 뷰"""
    model = Report
    template_name = 'community/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = Report.objects.select_related(
            'reporter', 'post', 'comment', 'reviewed_by'
        ).order_by('-created_at')
        
        # 상태 필터링
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # 신고 유형 필터링
        report_type = self.request.GET.get('report_type')
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Report.REPORT_STATUS
        context['type_choices'] = Report.REPORT_TYPES
        context['current_status'] = self.request.GET.get('status', '')
        context['current_type'] = self.request.GET.get('report_type', '')
        
        # 통계 정보
        context['pending_count'] = Report.objects.filter(status='PENDING').count()
        context['reviewing_count'] = Report.objects.filter(status='REVIEWING').count()
        context['resolved_count'] = Report.objects.filter(status='RESOLVED').count()
        context['rejected_count'] = Report.objects.filter(status='REJECTED').count()
        
        return context

class ReportDetailView(UserPassesTestMixin, DetailView):
    """관리자용 신고 상세 뷰"""
    model = Report
    template_name = 'community/report_detail.html'
    context_object_name = 'report'
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_staff

class ReportUpdateStatusView(UserPassesTestMixin, View):
    """신고 상태 업데이트 뷰 (AJAX)"""
    raise_exception = True
    
    def test_func(self):
        return self.request.user.is_staff
    
    def post(self, request, *args, **kwargs):
        try:
            report_id = kwargs.get('pk')
            report = get_object_or_404(Report, id=report_id)
            
            status = request.POST.get('status')
            admin_note = request.POST.get('admin_note', '')
            
            if status not in dict(Report.REPORT_STATUS).keys():
                return JsonResponse({
                    'success': False,
                    'message': '유효하지 않은 상태입니다.'
                }, status=400)
            
            report.status = status
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            if admin_note:
                report.admin_note = admin_note
            report.save()
            
            # 신고가 해결됨으로 처리되고 게시글/댓글 삭제 옵션이 선택된 경우
            delete_content = request.POST.get('delete_content') == 'true'
            if status == 'RESOLVED' and delete_content:
                if report.post:
                    report.post.delete()
                elif report.comment:
                    report.comment.delete()
            
            return JsonResponse({
                'success': True,
                'message': '신고 처리가 완료되었습니다.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'처리 중 오류가 발생했습니다: {str(e)}'
            }, status=500)
