from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, FileResponse, Http404
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Subject, TimeSlot, Semester, SubjectFile
from .forms import SubjectForm, TimeSlotForm, SubjectWithTimeSlotsForm, SemesterForm, ImprovedSubjectWithTimeSlotsForm, SubjectFileForm

class TimetableView(LoginRequiredMixin, TemplateView):
    """시간표 메인 뷰"""
    template_name = 'timetable/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 현재 학기 가져오기
        current_semester = Semester.objects.filter(user=user, is_current=True).first()
        
        # 모든 과목 가져오기 (학기 구분 없이)
        semester_subjects = Subject.objects.filter(user=user).prefetch_related('time_slots')
        semester_subjects_count = semester_subjects.count()
        
        # 시간표 데이터 구성
        timetable_data = {}
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        periods = range(1, 9)  # 1교시부터 8교시까지
        
        # 빈 시간표 초기화
        for day in days:
            timetable_data[day] = {}
            for period in periods:
                timetable_data[day][period] = None
        
        # 시간표에 과목 배치 (모든 과목)
        for subject in semester_subjects:
            for time_slot in subject.time_slots.all():
                if time_slot.day in timetable_data and time_slot.period in periods:
                    timetable_data[time_slot.day][time_slot.period] = {
                        'subject': subject,
                        'time_slot': time_slot
                    }
        
        context.update({
            'current_semester': current_semester,
            'semester_subjects': semester_subjects,  # 모든 과목 목록
            'semester_subjects_count': semester_subjects_count,  # 모든 과목 개수
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'day_names': {
                'MON': '월요일', 
                'TUE': '화요일', 
                'WED': '수요일', 
                'THU': '목요일', 
                'FRI': '금요일'
            }
        })
        return context

class SubjectCreateView(LoginRequiredMixin, CreateView):
    """과목 생성 뷰"""
    model = Subject
    form_class = SubjectWithTimeSlotsForm
    template_name = 'timetable/subject_create.html'
    success_url = reverse_lazy('timetable:index')
    
    def form_valid(self, form):
        with transaction.atomic():
            # 과목 저장
            form.instance.user = self.request.user
            subject = form.save()
            
            # 시간표 슬롯 생성
            days = form.cleaned_data['days']
            periods = form.cleaned_data['periods']
            location = form.cleaned_data['location']
            
            for day in days:
                for period in periods:
                    TimeSlot.objects.create(
                        subject=subject,
                        day=day,
                        period=int(period),
                        location=location
                    )
            
            messages.success(self.request, f'"{subject.name}" 과목이 성공적으로 추가되었습니다.')
            return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, '과목 추가 중 오류가 발생했습니다. 입력 정보를 확인해주세요.')
        return super().form_invalid(form)

class SubjectDetailView(LoginRequiredMixin, DetailView):
    """과목 상세 뷰"""
    model = Subject
    template_name = 'timetable/subject_detail.html'
    context_object_name = 'subject'
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user).prefetch_related('time_slots', 'files')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = self.object.files.all()
        return context

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    """과목 수정 뷰"""
    model = Subject
    form_class = SubjectForm
    template_name = 'timetable/subject_edit.html'
    success_url = reverse_lazy('timetable:subject_list')
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'"{form.instance.name}" 과목이 성공적으로 수정되었습니다.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '과목 수정 중 오류가 발생했습니다. 입력 내용을 확인해주세요.')
        return super().form_invalid(form)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    """과목 삭제 뷰"""
    model = Subject
    template_name = 'timetable/subject_delete.html'
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        # HTTP_REFERER에서 이전 페이지 확인하여 적절한 페이지로 리다이렉트
        referer = self.request.session.get('delete_referer', '')
        if 'manage' in referer:
            return reverse_lazy('timetable:timetable_manage')
        return reverse_lazy('timetable:index')
    
    def get(self, request, *args, **kwargs):
        # 삭제 확인 페이지 접근 시 이전 페이지 저장
        referer = request.META.get('HTTP_REFERER', '')
        request.session['delete_referer'] = referer
        return super().get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        subject = self.get_object()
        subject_name = subject.name
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'"{subject_name}" 과목이 삭제되었습니다.')
        return result

class SemesterListView(LoginRequiredMixin, ListView):
    """학기 목록 뷰"""
    model = Semester
    template_name = 'timetable/semester_list.html'
    context_object_name = 'semesters'
    
    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user)

class SemesterCreateView(LoginRequiredMixin, CreateView):
    """학기 생성 뷰"""
    model = Semester
    form_class = SemesterForm
    template_name = 'timetable/semester_create.html'
    success_url = reverse_lazy('timetable:semester_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '새 학기가 추가되었습니다.')
        return super().form_valid(form)

class TimeSlotCreateView(LoginRequiredMixin, CreateView):
    """시간표 슬롯 추가 뷰 (AJAX)"""
    model = TimeSlot
    form_class = TimeSlotForm
    
    def post(self, request, *args, **kwargs):
        subject_id = kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id, user=request.user)
        
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            time_slot = form.save(commit=False)
            time_slot.subject = subject
            
            # 중복 시간 체크
            existing_slot = TimeSlot.objects.filter(
                subject__user=request.user,
                day=time_slot.day,
                period=time_slot.period
            ).exclude(subject=subject).first()
            
            if existing_slot:
                return JsonResponse({
                    'success': False,
                    'error': f'{time_slot.get_day_display()} {time_slot.get_period_display()}에 이미 "{existing_slot.subject.name}" 과목이 있습니다.'
                })
            
            time_slot.save()
            return JsonResponse({
                'success': True,
                'message': '시간표가 추가되었습니다.'
            })
        
        return JsonResponse({
            'success': False,
            'error': '입력 정보를 확인해주세요.'
        })

class SubjectListView(LoginRequiredMixin, ListView):
    """과목 목록 뷰"""
    model = Subject
    template_name = 'timetable/subject_list.html'
    context_object_name = 'subjects'
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user).prefetch_related('time_slots')

class SubjectOnlyCreateView(LoginRequiredMixin, CreateView):
    """과목만 생성하는 뷰 (시간표 없이)"""
    model = Subject
    form_class = SubjectForm
    template_name = 'timetable/subject_only_create.html'
    success_url = reverse_lazy('timetable:subject_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'"{form.instance.name}" 과목이 추가되었습니다.')
        return super().form_valid(form)

class TimetableManageView(LoginRequiredMixin, TemplateView):
    """시간표 관리 뷰 (과목을 시간표에 추가/제거)"""
    template_name = 'timetable/timetable_manage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 사용자의 모든 과목
        subjects = Subject.objects.filter(user=user).prefetch_related('time_slots')
        
        # 시간표 데이터 구성
        timetable_data = {}
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        periods = range(1, 9)
        
        # 빈 시간표 초기화
        for day in days:
            timetable_data[day] = {}
            for period in periods:
                timetable_data[day][period] = None
        
        # 시간표에 과목 배치
        for subject in subjects:
            for time_slot in subject.time_slots.all():
                if time_slot.day in timetable_data and time_slot.period in periods:
                    timetable_data[time_slot.day][time_slot.period] = {
                        'subject': subject,
                        'time_slot': time_slot
                    }
        
        context.update({
            'subjects': subjects,
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'day_names': {
                'MON': '월요일',
                'TUE': '화요일', 
                'WED': '수요일',
                'THU': '목요일',
                'FRI': '금요일'
            },
            'period_times': {
                1: '08:10-09:00',
                2: '09:10-10:00',
                3: '10:10-11:00',
                4: '11:10-12:00',
                5: '13:00-13:50',
                6: '14:00-14:50',
                7: '15:10-16:00',
                8: '16:10-17:00',
            }
        })
        return context

def add_to_timetable(request):
    """AJAX: 과목을 시간표에 추가"""
    if request.method == 'POST':
        try:
            subject_id = request.POST.get('subject_id')
            day = request.POST.get('day')
            period_str = request.POST.get('period')
            location = request.POST.get('location', '')
            
            # 입력값 검증
            if not subject_id:
                return JsonResponse({
                    'success': False,
                    'error': '과목을 선택해주세요.'
                })
            
            if not day:
                return JsonResponse({
                    'success': False,
                    'error': '요일을 선택해주세요.'
                })
            
            if not period_str:
                return JsonResponse({
                    'success': False,
                    'error': '교시를 선택해주세요.'
                })
            
            try:
                period = int(period_str)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': '올바른 교시를 선택해주세요.'
                })
            
            # 과목 조회
            try:
                subject = Subject.objects.get(id=subject_id, user=request.user)
            except Subject.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': '선택한 과목을 찾을 수 없습니다.'
                })
            
            # 중복 시간 체크 (다른 과목과의 충돌만 체크)
            existing_slot = TimeSlot.objects.filter(
                subject__user=request.user,
                day=day,
                period=period
            ).exclude(subject=subject).first()
            
            if existing_slot:
                return JsonResponse({
                    'success': False,
                    'error': f'해당 시간에 이미 "{existing_slot.subject.name}" 과목이 있습니다.'
                })
            
            # 같은 과목이 이미 해당 시간에 있는지 체크
            same_subject_slot = TimeSlot.objects.filter(
                subject=subject,
                day=day,
                period=period
            ).first()
            
            if same_subject_slot:
                return JsonResponse({
                    'success': False,
                    'error': f'"{subject.name}" 과목이 이미 해당 시간에 배치되어 있습니다.'
                })
            
            # 시간표 슬롯 생성
            TimeSlot.objects.create(
                subject=subject,
                day=day,
                period=period,
                location=location
            )
            
            return JsonResponse({
                'success': True,
                'message': f'"{subject.name}" 과목이 {day} {period}교시에 추가되었습니다.',
                'subject_name': subject.name,
                'subject_color': subject.color
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'서버 오류가 발생했습니다: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청 방식입니다.'})

def remove_from_timetable(request):
    """AJAX: 시간표에서 과목 제거"""
    if request.method == 'POST':
        day = request.POST.get('day')
        period = int(request.POST.get('period'))
        
        try:
            time_slot = TimeSlot.objects.get(
                subject__user=request.user,
                day=day,
                period=period
            )
            subject_name = time_slot.subject.name
            time_slot.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'"{subject_name}" 과목이 시간표에서 제거되었습니다.'
            })
            
        except TimeSlot.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': '해당 시간표 슬롯을 찾을 수 없습니다.'
            })
    
    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})


@login_required
@require_http_methods(["GET"])
def get_timetable_data(request):
    """시간표 데이터를 JSON으로 반환하는 API"""
    try:
        user = request.user
        
        # 사용자의 모든 과목과 시간표 데이터 가져오기
        subjects = Subject.objects.filter(user=user).prefetch_related('time_slots')
        
        timetable_data = []
        for subject in subjects:
            for time_slot in subject.time_slots.all():
                timetable_data.append({
                    'day': time_slot.day,
                    'period': time_slot.period,
                    'subject_name': subject.name,
                    'subject_color': subject.color or '#007bff',
                    'subject_id': subject.id,
                    'time_slot_id': time_slot.id
                })
        
        return JsonResponse({
            'success': True,
            'timetable_data': timetable_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

class ImprovedSubjectCreateView(LoginRequiredMixin, CreateView):
    """과목만 생성하는 뷰 (시간표 없이) - subject_create와 동일"""
    model = Subject
    form_class = SubjectForm
    template_name = 'timetable/subject_create_improved.html'
    success_url = reverse_lazy('timetable:subject_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'"{form.instance.name}" 과목이 추가되었습니다.')
        return super().form_valid(form)

class SubjectFileUploadView(LoginRequiredMixin, CreateView):
    """과목 파일 업로드 뷰"""
    model = SubjectFile
    form_class = SubjectFileForm
    template_name = 'timetable/subject_file_upload.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.subject = get_object_or_404(Subject, pk=kwargs['subject_id'], user=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context
    
    def form_valid(self, form):
        form.instance.subject = self.subject
        messages.success(self.request, f'"{form.instance.title}" 파일이 업로드되었습니다.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('timetable:subject_detail', kwargs={'pk': self.subject.pk})

class SubjectFileDeleteView(LoginRequiredMixin, DeleteView):
    """과목 파일 삭제 뷰"""
    model = SubjectFile
    template_name = 'timetable/subject_file_delete.html'
    
    def get_queryset(self):
        return SubjectFile.objects.filter(subject__user=self.request.user)
    
    def get_success_url(self):
        return reverse('timetable:subject_detail', kwargs={'pk': self.object.subject.pk})
    
    def delete(self, request, *args, **kwargs):
        file_obj = self.get_object()
        file_title = file_obj.title
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f'"{file_title}" 파일이 삭제되었습니다.')
        return result

@login_required
def download_subject_file(request, pk):
    """과목 파일 다운로드"""
    file_obj = get_object_or_404(SubjectFile, pk=pk, subject__user=request.user)
    
    try:
        response = FileResponse(file_obj.file.open('rb'), as_attachment=True, filename=file_obj.file.name.split('/')[-1])
        return response
    except Exception as e:
        messages.error(request, '파일 다운로드 중 오류가 발생했습니다.')
        return redirect('timetable:subject_detail', pk=file_obj.subject.pk)