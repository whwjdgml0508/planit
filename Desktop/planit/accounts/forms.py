from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit, HTML
from crispy_forms.bootstrap import PrependedText

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """사용자 회원가입 폼"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='이름',
        widget=forms.TextInput(attrs={'placeholder': '이름을 입력하세요'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='성',
        widget=forms.TextInput(attrs={'placeholder': '성을 입력하세요'})
    )
    email = forms.EmailField(
        required=True,
        label='이메일',
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com'})
    )
    student_id = forms.CharField(
        max_length=7,
        required=True,
        label='학번',
        widget=forms.TextInput(attrs={'placeholder': '1234567'})
    )
    department = forms.ChoiceField(
        choices=User.DEPARTMENT_CHOICES,
        required=True,
        label='학과'
    )
    grade = forms.ChoiceField(
        choices=User.GRADE_CHOICES,
        required=True,
        label='학년'
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label='전화번호',
        widget=forms.TextInput(attrs={'placeholder': '010-1234-5678'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'student_id', 
                 'department', 'grade', 'phone_number', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('username', placeholder='사용자명'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('student_id', placeholder='학번'),
                    css_class='col-md-6'
                ),
                css_class='row mb-3'
            ),
            Div(
                Div(
                    Field('last_name', placeholder='성'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('first_name', placeholder='이름'),
                    css_class='col-md-6'
                ),
                css_class='row mb-3'
            ),
            Field('email', placeholder='이메일', css_class='mb-3'),
            Div(
                Div(
                    Field('department'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('grade'),
                    css_class='col-md-6'
                ),
                css_class='row mb-3'
            ),
            Field('phone_number', placeholder='전화번호 (선택사항)', css_class='mb-3'),
            Field('password1', placeholder='비밀번호', css_class='mb-3'),
            Field('password2', placeholder='비밀번호 확인', css_class='mb-3'),
            Submit('submit', '회원가입', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        self.fields['username'].label = '사용자명'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id and not student_id.isdigit():
            raise forms.ValidationError('학번은 숫자만 입력 가능합니다.')
        if student_id and len(student_id) != 7:
            raise forms.ValidationError('학번은 7자리여야 합니다.')
        return student_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용 중인 이메일입니다.')
        return email

class CustomAuthenticationForm(AuthenticationForm):
    """사용자 로그인 폼"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder='사용자명 또는 학번', css_class='mb-3'),
            Field('password', placeholder='비밀번호', css_class='mb-3'),
            Submit('submit', '로그인', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        self.fields['username'].label = '사용자명'
        self.fields['password'].label = '비밀번호'
        self.fields['username'].widget.attrs.update({'placeholder': '사용자명 또는 학번'})

class ProfileEditForm(forms.ModelForm):
    """프로필 수정 폼"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'department', 'grade', 
                 'phone_number', 'profile_image', 'bio')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('last_name', placeholder='성'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('first_name', placeholder='이름'),
                    css_class='col-md-6'
                ),
                css_class='row mb-3'
            ),
            Field('email', placeholder='이메일', css_class='mb-3'),
            Div(
                Div(
                    Field('department'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('grade'),
                    css_class='col-md-6'
                ),
                css_class='row mb-3'
            ),
            Field('phone_number', placeholder='전화번호', css_class='mb-3'),
            Field('profile_image', css_class='mb-3'),
            Field('bio', rows=4, placeholder='자기소개를 입력하세요', css_class='mb-3'),
            Submit('submit', '프로필 업데이트', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        
        # 필드 라벨 설정
        for field_name, field in self.fields.items():
            if hasattr(User._meta.get_field(field_name), 'verbose_name'):
                field.label = User._meta.get_field(field_name).verbose_name
