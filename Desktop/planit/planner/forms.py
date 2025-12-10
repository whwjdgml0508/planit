from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML, Row, Column
from .models import Task, StudySession, Goal
from timetable.models import Subject

class TaskForm(forms.ModelForm):
    """과제/할일 생성/수정 폼"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 
                 'due_date', 'estimated_hours', 'subject', 'progress']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # 사용자의 과목만 선택 가능하도록 필터링
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', placeholder='과제 제목'),
            Field('description', placeholder='과제에 대한 상세 설명을 입력하세요'),
            Row(
                Column(
                    Field('category'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('priority'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('status'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('progress'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('due_date'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('estimated_hours'),
                    css_class='col-md-6'
                ),
            ),
            Field('subject'),
            Submit('submit', '저장', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['title'].label = '제목'
        self.fields['description'].label = '설명'
        self.fields['category'].label = '카테고리'
        self.fields['priority'].label = '우선순위'
        self.fields['status'].label = '상태'
        self.fields['due_date'].label = '마감일'
        self.fields['estimated_hours'].label = '예상 소요시간(시간)'
        self.fields['subject'].label = '관련 과목'
        self.fields['progress'].label = '진행률(%)'
        
        # 빈 옵션 추가
        self.fields['subject'].empty_label = "과목 선택 (선택사항)"
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date <= timezone.now():
            raise forms.ValidationError('마감일은 현재 시간보다 늦어야 합니다.')
        return due_date

class StudySessionForm(forms.ModelForm):
    """학습 세션 폼"""
    
    class Meta:
        model = StudySession
        fields = ['title', 'description', 'task', 'subject', 'start_time', 
                 'end_time', 'effectiveness_rating', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # 사용자의 과제와 과목만 선택 가능하도록 필터링
            self.fields['task'].queryset = Task.objects.filter(user=user, status__in=['TODO', 'IN_PROGRESS'])
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', placeholder='학습 세션 제목'),
            Field('description', placeholder='학습 내용을 간단히 설명하세요'),
            Row(
                Column(
                    Field('task'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('subject'),
                    css_class='col-md-6'
                ),
            ),
            Row(
                Column(
                    Field('start_time'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('end_time'),
                    css_class='col-md-6'
                ),
            ),
            Field('effectiveness_rating'),
            Field('notes', placeholder='학습 중 메모나 느낀 점을 기록하세요'),
            Submit('submit', '저장', css_class='btn btn-success btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['title'].label = '세션 제목'
        self.fields['description'].label = '학습 내용'
        self.fields['task'].label = '관련 과제'
        self.fields['subject'].label = '관련 과목'
        self.fields['start_time'].label = '시작 시간'
        self.fields['end_time'].label = '종료 시간'
        self.fields['effectiveness_rating'].label = '효과성 평가 (1-5점)'
        self.fields['notes'].label = '학습 노트'
        
        # 빈 옵션 추가
        self.fields['task'].empty_label = "과제 선택 (선택사항)"
        self.fields['subject'].empty_label = "과목 선택 (선택사항)"
        
        # 기본값 설정
        if not self.instance.pk:
            self.fields['start_time'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError('종료 시간은 시작 시간보다 늦어야 합니다.')
            
            # 24시간을 초과하는 세션 방지
            duration = end_time - start_time
            if duration.total_seconds() > 24 * 60 * 60:
                raise forms.ValidationError('학습 세션은 24시간을 초과할 수 없습니다.')
        
        return cleaned_data

class GoalForm(forms.ModelForm):
    """학습 목표 폼"""
    
    class Meta:
        model = Goal
        fields = ['title', 'description', 'goal_type', 'start_date', 'end_date',
                 'target_hours', 'target_tasks']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('title', placeholder='목표 제목'),
            Field('description', placeholder='목표에 대한 상세 설명을 입력하세요'),
            Field('goal_type'),
            Row(
                Column(
                    Field('start_date'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('end_date'),
                    css_class='col-md-6'
                ),
            ),
            HTML('<hr class="my-3">'),
            HTML('<h6 class="mb-3">목표 수치 설정 (선택사항)</h6>'),
            Row(
                Column(
                    Field('target_hours'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('target_tasks'),
                    css_class='col-md-6'
                ),
            ),
            Submit('submit', '목표 설정', css_class='btn btn-warning btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['title'].label = '목표 제목'
        self.fields['description'].label = '목표 설명'
        self.fields['goal_type'].label = '목표 유형'
        self.fields['start_date'].label = '시작일'
        self.fields['end_date'].label = '종료일'
        self.fields['target_hours'].label = '목표 학습시간 (시간, 선택사항)'
        self.fields['target_tasks'].label = '목표 과제 수 (선택사항)'
        
        # 기본값 설정
        if not self.instance.pk:
            today = timezone.now().date()
            self.fields['start_date'].initial = today
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        target_hours = cleaned_data.get('target_hours')
        target_tasks = cleaned_data.get('target_tasks')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('종료일은 시작일보다 늦어야 합니다.')
        
        return cleaned_data

class TaskFilterForm(forms.Form):
    """과제 필터링 폼"""
    
    STATUS_CHOICES = [('', '전체')] + Task.STATUS_CHOICES
    PRIORITY_CHOICES = [('', '전체')] + Task.PRIORITY_CHOICES
    CATEGORY_CHOICES = [('', '전체')] + Task.CATEGORY_CHOICES
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.none(), required=False, empty_label="전체")
    overdue_only = forms.BooleanField(required=False, label='마감일 지난 것만')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column(Field('status'), css_class='col-md-2'),
                Column(Field('priority'), css_class='col-md-2'),
                Column(Field('category'), css_class='col-md-2'),
                Column(Field('subject'), css_class='col-md-3'),
                Column(Field('overdue_only'), css_class='col-md-2'),
                Column(Submit('filter', '필터 적용', css_class='btn btn-outline-primary'), css_class='col-md-1'),
            )
        )
