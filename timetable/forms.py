from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML, Row, Column
from crispy_forms.bootstrap import PrependedText
from .models import Subject, TimeSlot, Semester

class SubjectForm(forms.ModelForm):
    """과목 생성/수정 폼"""
    
    class Meta:
        model = Subject
        fields = ['name', 'professor', 'credits', 'subject_type', 
                 'evaluation_method', 'classroom', 'note', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'note': forms.Textarea(attrs={'rows': 3}),
            'evaluation_method': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', placeholder='과목명', css_class='mb-3'),
            Row(
                Column(
                    Field('professor', placeholder='교수명'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('credits'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Row(
                Column(
                    Field('subject_type'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('evaluation_method', placeholder='예: 중간고사 30%, 기말고사 40%, 과제 20%, 출석 10%'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Row(
                Column(
                    Field('classroom', placeholder='강의실'),
                    css_class='col-md-8'
                ),
                Column(
                    Field('color'),
                    css_class='col-md-4'
                ),
                css_class='mb-3'
            ),
            Field('note', placeholder='과목에 대한 메모를 입력하세요', css_class='mb-3'),
            Submit('submit', '저장', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['name'].label = '과목명'
        self.fields['professor'].label = '교수명'
        self.fields['credits'].label = '학점'
        self.fields['subject_type'].label = '과목 구분'
        self.fields['evaluation_method'].label = '평가 방식'
        self.fields['classroom'].label = '강의실'
        self.fields['note'].label = '메모'
        self.fields['color'].label = '색상'

class TimeSlotForm(forms.ModelForm):
    """시간표 슬롯 폼"""
    
    class Meta:
        model = TimeSlot
        fields = ['day', 'period', 'location', 'note']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('day'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('period'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Field('location', placeholder='장소', css_class='mb-3'),
            Field('note', placeholder='시간표 슬롯에 대한 메모', css_class='mb-3'),
            Submit('submit', '추가', css_class='btn btn-success w-100 mt-3')
        )
        
        self.fields['day'].label = '요일'
        self.fields['period'].label = '교시'
        self.fields['location'].label = '장소'
        self.fields['note'].label = '메모'

# TimeSlot 인라인 폼셋
TimeSlotFormSet = inlineformset_factory(
    Subject, 
    TimeSlot,
    form=TimeSlotForm,
    fields=['day', 'period', 'location', 'note'],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class SubjectWithTimeSlotsForm(forms.ModelForm):
    """과목과 시간표를 함께 생성하는 폼"""
    
    # 시간표 정보
    days = forms.MultipleChoiceField(
        choices=TimeSlot.DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='요일'
    )
    periods = forms.MultipleChoiceField(
        choices=TimeSlot.PERIOD_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='교시'
    )
    location = forms.CharField(
        max_length=50,
        required=False,
        label='장소',
        widget=forms.TextInput(attrs={'placeholder': '강의실 또는 장소'})
    )
    
    class Meta:
        model = Subject
        fields = ['name', 'professor', 'credits', 'subject_type', 
                 'evaluation_method', 'classroom', 'note', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'note': forms.Textarea(attrs={'rows': 3}),
            'evaluation_method': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h5 class="mb-3">📚 과목 정보</h5>'),
            Field('name', placeholder='과목명', css_class='mb-3'),
            Row(
                Column(
                    Field('professor', placeholder='교수명'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('credits'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Field('subject_type', css_class='mb-3'),
            Field('evaluation_method', placeholder='예: 중간고사 30%, 기말고사 40%, 과제 20%, 출석 10%', css_class='mb-3'),
            Row(
                Column(
                    Field('classroom', placeholder='강의실'),
                    css_class='col-md-8'
                ),
                Column(
                    Field('color'),
                    css_class='col-md-4'
                ),
                css_class='mb-3'
            ),
            Field('note', placeholder='과목에 대한 메모를 입력하세요', css_class='mb-3'),
            
            HTML('<hr class="my-4">'),
            HTML('<h5 class="mb-3">📅 시간표 정보</h5>'),
            
            Row(
                Column(
                    Field('days'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('periods'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Field('location', placeholder='장소', css_class='mb-3'),
            
            Submit('submit', '과목 및 시간표 저장', css_class='btn btn-primary btn-lg w-100 mt-4')
        )

class SemesterForm(forms.ModelForm):
    """학기 폼"""
    
    class Meta:
        model = Semester
        fields = ['year', 'semester', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('year'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('semester'),
                    css_class='col-md-6'
                ),
            ),
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
            Field('is_current'),
            Submit('submit', '학기 저장', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        self.fields['year'].label = '년도'
        self.fields['semester'].label = '학기'
        self.fields['start_date'].label = '시작일'
        self.fields['end_date'].label = '종료일'
        self.fields['is_current'].label = '현재 학기로 설정'
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError('시작일은 종료일보다 빨라야 합니다.')
        
        return cleaned_data
