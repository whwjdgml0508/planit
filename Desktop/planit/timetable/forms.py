from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML, Row, Column
from crispy_forms.bootstrap import PrependedText
from .models import Subject, TimeSlot, Semester, SubjectFile

class SubjectForm(forms.ModelForm):
    """과목 생성/수정 폼"""
    
    midterm_percent = forms.IntegerField(
        required=False,
        initial=0,
        min_value=0,
        max_value=100,
        label='중간',
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    final_percent = forms.IntegerField(
        required=False,
        initial=0,
        min_value=0,
        max_value=100,
        label='기말',
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    quiz_percent = forms.IntegerField(
        required=False,
        initial=0,
        min_value=0,
        max_value=100,
        label='수시',
        widget=forms.NumberInput(attrs={'placeholder': '0', 'class': 'form-control'})
    )
    
    class Meta:
        model = Subject
        fields = ['name', 'professor', 'credits', 'subject_type', 
                 'semester', 'classroom', 'note', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.evaluation_method:
            eval_text = instance.evaluation_method
            import re
            midterm_match = re.search(r'중간[^0-9]*(\d+)', eval_text)
            final_match = re.search(r'기말[^0-9]*(\d+)', eval_text)
            quiz_match = re.search(r'수시[^0-9]*(\d+)', eval_text)
            
            if midterm_match:
                kwargs['initial'] = kwargs.get('initial', {})
                kwargs['initial']['midterm_percent'] = int(midterm_match.group(1))
            if final_match:
                kwargs['initial'] = kwargs.get('initial', {})
                kwargs['initial']['final_percent'] = int(final_match.group(1))
            if quiz_match:
                kwargs['initial'] = kwargs.get('initial', {})
                kwargs['initial']['quiz_percent'] = int(quiz_match.group(1))
        
        super().__init__(*args, **kwargs)
        
        # 사용자별 학기 필터링
        user = kwargs.get('initial', {}).get('user') or (instance.user if instance else None)
        if user:
            self.fields['semester'].queryset = Semester.objects.filter(user=user).order_by('-year', '-semester')
        
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
                    Field('semester'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('subject_type'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Row(
                Column(
                    HTML('<label class="form-label">평가 방식</label>'),
                    Row(
                        Column(Field('midterm_percent'), css_class='col-4'),
                        Column(Field('final_percent'), css_class='col-4'),
                        Column(Field('quiz_percent'), css_class='col-4'),
                    ),
                    css_class='col-md-12'
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
        
        self.fields['name'].label = '과목명'
        self.fields['professor'].label = '교수명'
        self.fields['credits'].label = '학점'
        self.fields['credits'].required = False
        self.fields['subject_type'].label = '과목 구분'
        self.fields['classroom'].label = '강의실'
        self.fields['note'].label = '메모'
        self.fields['color'].label = '색상'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        midterm = self.cleaned_data.get('midterm_percent', 0) or 0
        final = self.cleaned_data.get('final_percent', 0) or 0
        quiz = self.cleaned_data.get('quiz_percent', 0) or 0
        
        eval_parts = []
        if midterm > 0:
            eval_parts.append(f'중간고사 {midterm}%')
        if final > 0:
            eval_parts.append(f'기말고사 {final}%')
        if quiz > 0:
            eval_parts.append(f'수시 {quiz}%')
        
        instance.evaluation_method = ', '.join(eval_parts) if eval_parts else ''
        
        if commit:
            instance.save()
        return instance

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
        self.user = kwargs.pop('user', None)
        self.current_semester = kwargs.pop('current_semester', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="form-section"><h5><i class="fas fa-book me-2"></i>📚 과목 정보</h5>'),
            Row(
                Column(
                    Field('name', placeholder='과목명 입력', css_class='mb-3'),
                    css_class='col-md-9'
                ),
                Column(
                    Field('credits', css_class='mb-3'),
                    css_class='col-md-3'
                ),
            ),
            Row(
                Column(
                    Field('professor', placeholder='교수명 입력'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('subject_type'),
                    css_class='col-md-6'
                ),
                css_class='mb-3'
            ),
            Field('evaluation_method', placeholder='예: 중간고사 30%, 기말고사 40%, 과제 20%, 출석 10%', css_class='mb-3'),
            Row(
                Column(
                    Field('classroom', placeholder='강의실 입력'),
                    css_class='col-md-8'
                ),
                Column(
                    Field('color'),
                    css_class='col-md-4'
                ),
                css_class='mb-3'
            ),
            Field('note', placeholder='과목에 대한 메모를 입력하세요', css_class='mb-3'),
            HTML('</div>'),
            
            HTML('<div class="form-section mt-4"><h5><i class="fas fa-calendar-alt me-2"></i>📅 시간표 선택</h5>'),
            HTML('<p class="text-muted small mb-3"><i class="fas fa-info-circle me-1"></i>원하는 요일과 교시를 모두 선택하세요. 선택한 모든 시간에 과목이 배치됩니다.</p>'),
            
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
            Field('location', placeholder='강의실 또는 장소 입력', css_class='mb-3'),
            HTML('</div>'),
            
            Submit('submit', '✓ 과목 및 시간표 저장', css_class='btn btn-submit w-100 mt-4')
        )
    
    def clean(self):
        cleaned_data = super().clean()
        days = cleaned_data.get('days')
        periods = cleaned_data.get('periods')
        
        if not days or not periods:
            return cleaned_data
        
        # 현재 학기에서 시간표 충돌 체크
        if self.user and self.current_semester:
            conflicts = []
            for day in days:
                for period in periods:
                    # 현재 학기에서 해당 시간에 이미 다른 과목이 있는지 체크
                    existing_slot = TimeSlot.objects.filter(
                        subject__user=self.user,
                        semester=self.current_semester,
                        day=day,
                        period=int(period)
                    ).select_related('subject').first()
                    
                    if existing_slot:
                        day_name = dict(TimeSlot.DAY_CHOICES).get(day, day)
                        period_name = dict(TimeSlot.PERIOD_CHOICES).get(int(period), period)
                        conflicts.append(
                            f"{day_name} {period_name}: '{existing_slot.subject.name}' 과목이 이미 배치되어 있습니다."
                        )
            
            if conflicts:
                raise forms.ValidationError(
                    "선택한 시간에 이미 다른 과목이 있습니다:\n" + "\n".join(conflicts)
                )
        
        return cleaned_data

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

class TimeSlotSelectionForm(forms.Form):
    """시간표 그리드 선택 폼 - 여러 시간대를 동시에 선택 가능"""
    
    # 동적으로 생성될 체크박스 필드들
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 각 요일과 교시 조합에 대한 체크박스 생성
        for day_code, day_name in TimeSlot.DAY_CHOICES:
            for period_num, period_name in TimeSlot.PERIOD_CHOICES:
                field_name = f'slot_{day_code}_{period_num}'
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=f'{day_name} {period_name}',
                    widget=forms.CheckboxInput(attrs={
                        'class': 'time-slot-checkbox',
                        'data-day': day_code,
                        'data-period': period_num
                    })
                )
        
        # 추가 정보 필드
        self.fields['location'] = forms.CharField(
            max_length=50,
            required=False,
            label='장소',
            widget=forms.TextInput(attrs={'placeholder': '강의실 또는 장소'})
        )
        
        self.fields['note'] = forms.CharField(
            required=False,
            label='메모',
            widget=forms.Textarea(attrs={'rows': 2, 'placeholder': '시간표에 대한 메모'})
        )
    
    def get_selected_slots(self):
        """선택된 시간대 목록 반환"""
        selected_slots = []
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('slot_') and value:
                # slot_MON_1 형태에서 요일과 교시 추출
                parts = field_name.split('_')
                if len(parts) == 3:
                    day = parts[1]
                    period = int(parts[2])
                    selected_slots.append({'day': day, 'period': period})
        return selected_slots

class ImprovedSubjectWithTimeSlotsForm(forms.ModelForm):
    """개선된 과목과 시간표 생성 폼 - 시간표 그리드 선택 방식"""
    
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
        
        # 시간표 선택 필드들 추가
        for day_code, day_name in TimeSlot.DAY_CHOICES:
            for period_num, period_name in TimeSlot.PERIOD_CHOICES:
                field_name = f'slot_{day_code}_{period_num}'
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=f'{day_name} {period_name}',
                    widget=forms.CheckboxInput(attrs={
                        'class': 'time-slot-checkbox',
                        'data-day': day_code,
                        'data-period': period_num
                    })
                )
        
        # 시간표 공통 정보
        self.fields['timeslot_location'] = forms.CharField(
            max_length=50,
            required=False,
            label='시간표 장소',
            widget=forms.TextInput(attrs={'placeholder': '강의실 또는 장소'})
        )
        
        self.fields['timeslot_note'] = forms.CharField(
            required=False,
            label='시간표 메모',
            widget=forms.Textarea(attrs={'rows': 2, 'placeholder': '시간표에 대한 메모'})
        )
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'improved-subject-form'
        
        # 필드 라벨 설정
        self.fields['name'].label = '과목명'
        self.fields['professor'].label = '교수명'
        self.fields['credits'].label = '학점'
        self.fields['credits'].required = False
        self.fields['subject_type'].label = '과목 구분'
        self.fields['evaluation_method'].label = '평가 방식'
        self.fields['classroom'].label = '강의실'
        self.fields['note'].label = '메모'
        self.fields['color'].label = '색상'
    
    def get_selected_slots(self):
        """선택된 시간대 목록 반환"""
        selected_slots = []
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('slot_') and value:
                parts = field_name.split('_')
                if len(parts) == 3:
                    day = parts[1]
                    period = int(parts[2])
                    selected_slots.append({'day': day, 'period': period})
        return selected_slots

class SubjectFileForm(forms.ModelForm):
    """과목 파일 업로드 폼"""
    
    class Meta:
        model = SubjectFile
        fields = ['file_type', 'title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file_type'].label = '파일 종류'
        self.fields['title'].label = '파일 제목'
        self.fields['description'].label = '설명'
        self.fields['file'].label = '파일'
        
        self.fields['title'].widget.attrs.update({'placeholder': '예: 1주차 강의자료, 중간고사 범위 등'})
        self.fields['description'].widget.attrs.update({'placeholder': '파일에 대한 간단한 설명 (선택사항)'})
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError('파일 크기는 50MB를 초과할 수 없습니다.')
        return file
