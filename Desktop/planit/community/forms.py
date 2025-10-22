from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML, Row, Column
from crispy_forms.bootstrap import PrependedText
from .models import Post, Comment, Category, Report, Attachment
from timetable.models import Subject

class PostForm(forms.ModelForm):
    """게시글 작성/수정 폼"""
    
    tags_input = forms.CharField(
        required=False,
        label='태그',
        help_text='태그를 쉼표(,)로 구분하여 입력하세요',
        widget=forms.TextInput(attrs={'placeholder': '예: 중간고사, 수학, 팁'})
    )
    
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'post_type', 'subject', 'tags_input']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # 사용자의 과목만 선택 가능하도록 필터링
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
            
            # 사용자 학과에 따른 카테고리 필터링
            categories = Category.objects.filter(is_active=True)
            if not user.is_staff:
                # 일반 사용자는 학과 제한이 있는 카테고리 필터링
                categories = categories.filter(
                    models.Q(department_restricted=False) |
                    models.Q(allowed_departments__contains=[user.department])
                )
            self.fields['category'].queryset = categories
        
        # 기존 태그 데이터 로드
        if self.instance.pk and self.instance.tags:
            self.fields['tags_input'].initial = ', '.join(self.instance.tags)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('category'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('post_type'),
                    css_class='col-md-6'
                ),
            ),
            PrependedText('title', '<i class="fas fa-heading"></i>', placeholder='게시글 제목을 입력하세요'),
            Field('subject'),
            Field('tags_input'),
            Field('content', placeholder='내용을 입력하세요...'),
            Submit('submit', '게시글 저장', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['category'].label = '카테고리'
        self.fields['title'].label = '제목'
        self.fields['content'].label = '내용'
        self.fields['post_type'].label = '게시글 유형'
        self.fields['subject'].label = '관련 과목'
        
        # 빈 옵션 추가
        self.fields['subject'].empty_label = "과목 선택 (선택사항)"
    
    def clean_tags_input(self):
        tags_input = self.cleaned_data.get('tags_input', '')
        if tags_input:
            # 태그를 쉼표로 분리하고 정리
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            # 중복 제거 및 최대 10개 제한
            tags = list(dict.fromkeys(tags))[:10]
            return tags
        return []
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # 태그 저장
        instance.tags = self.cleaned_data.get('tags_input', [])
        if commit:
            instance.save()
        return instance

class CommentForm(forms.ModelForm):
    """댓글 작성 폼"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '댓글을 입력하세요...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'comment-form'
        self.helper.layout = Layout(
            Field('content'),
            Submit('submit', '댓글 작성', css_class='btn btn-primary mt-2')
        )
        
        self.fields['content'].label = ''

class ReplyForm(forms.ModelForm):
    """대댓글 작성 폼"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': '답글을 입력하세요...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'reply-form'
        self.helper.layout = Layout(
            Field('content'),
            Submit('submit', '답글 작성', css_class='btn btn-sm btn-outline-primary mt-2')
        )
        
        self.fields['content'].label = ''

class PostSearchForm(forms.Form):
    """게시글 검색 폼"""
    
    SEARCH_TYPES = [
        ('all', '전체'),
        ('title', '제목'),
        ('content', '내용'),
        ('author', '작성자'),
        ('tags', '태그'),
    ]
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '검색어를 입력하세요'})
    )
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPES,
        required=False,
        initial='all'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="전체 카테고리"
    )
    post_type = forms.ChoiceField(
        choices=[('', '전체')] + Post.POST_TYPES,
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            # 일반 사용자는 접근 가능한 카테고리만 표시
            categories = Category.objects.filter(
                is_active=True
            ).filter(
                models.Q(department_restricted=False) |
                models.Q(allowed_departments__contains=[user.department])
            )
            self.fields['category'].queryset = categories
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'search-form'
        self.helper.layout = Layout(
            Row(
                Column(
                    PrependedText('query', '<i class="fas fa-search"></i>'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('search_type'),
                    css_class='col-md-2'
                ),
                Column(
                    Field('category'),
                    css_class='col-md-3'
                ),
                Column(
                    Field('post_type'),
                    css_class='col-md-2'
                ),
                Column(
                    Submit('search', '검색', css_class='btn btn-primary'),
                    css_class='col-md-1'
                ),
            )
        )

class ReportForm(forms.ModelForm):
    """신고 폼"""
    
    class Meta:
        model = Report
        fields = ['report_type', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('report_type'),
            Field('reason', placeholder='신고 사유를 상세히 입력해주세요'),
            Submit('submit', '신고하기', css_class='btn btn-danger w-100 mt-3')
        )
        
        self.fields['report_type'].label = '신고 유형'
        self.fields['reason'].label = '신고 사유'

class AttachmentForm(forms.ModelForm):
    """첨부파일 폼"""
    
    class Meta:
        model = Attachment
        fields = ['file']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['file'].label = '파일 첨부'
        self.fields['file'].help_text = '최대 10MB까지 업로드 가능합니다.'
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # 파일 크기 제한 (10MB)
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('파일 크기는 10MB를 초과할 수 없습니다.')
            
            # 허용된 파일 확장자 체크
            allowed_extensions = [
                '.jpg', '.jpeg', '.png', '.gif', '.bmp',  # 이미지
                '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.txt',  # 문서
                '.zip', '.rar', '.7z',  # 압축파일
            ]
            
            file_extension = file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError('지원하지 않는 파일 형식입니다.')
        
        return file
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if instance.file:
            # 원본 파일명 저장
            instance.original_name = instance.file.name
            instance.file_size = instance.file.size
            
            # 파일 유형 자동 감지
            file_extension = instance.file.name.lower().split('.')[-1]
            if file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                instance.file_type = 'IMAGE'
            elif file_extension in ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt']:
                instance.file_type = 'DOCUMENT'
            elif file_extension in ['zip', 'rar', '7z']:
                instance.file_type = 'ARCHIVE'
            else:
                instance.file_type = 'OTHER'
        
        if commit:
            instance.save()
        return instance

class CategoryForm(forms.ModelForm):
    """카테고리 관리 폼 (관리자용)"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'category_type', 'description', 'icon', 'color',
                 'is_active', 'order', 'department_restricted', 'allowed_departments']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    PrependedText('name', '<i class="fas fa-tag"></i>'),
                    css_class='col-md-6'
                ),
                Column(
                    PrependedText('slug', '<i class="fas fa-link"></i>'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('category_type'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('order'),
                    css_class='col-md-6'
                ),
            ),
            Field('description'),
            Row(
                Column(
                    PrependedText('icon', '<i class="fas fa-icons"></i>'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('color'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('is_active'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('department_restricted'),
                    css_class='col-md-8'
                ),
            ),
            Field('allowed_departments'),
            Submit('submit', '카테고리 저장', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
