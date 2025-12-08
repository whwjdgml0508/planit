from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
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
    
    def form_valid(self, form):
        messages.success(self.request, f'"{self.object.title}" 게시글이 수정되었습니다.')
        return super().form_valid(form)

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
        attachment_id = kwargs.get('pk')
        attachment = get_object_or_404(Attachment, id=attachment_id)
        
        # 다운로드 수 증가
        attachment.increment_download()
        
        # 파일 응답
        response = HttpResponse(attachment.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{attachment.original_name}"'
        return response

class ReportCreateView(LoginRequiredMixin, CreateView):
    """신고 생성 뷰"""
    model = Report
    form_class = ReportForm
    template_name = 'community/report_create.html'
    success_url = reverse_lazy('community:index')
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        
        # 게시글 또는 댓글 신고 처리
        post_id = self.request.GET.get('post')
        comment_id = self.request.GET.get('comment')
        
        if post_id:
            form.instance.post = get_object_or_404(Post, id=post_id)
        elif comment_id:
            form.instance.comment = get_object_or_404(Comment, id=comment_id)
        
        messages.success(self.request, '신고가 접수되었습니다. 검토 후 조치하겠습니다.')
        return super().form_valid(form)

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
