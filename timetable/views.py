from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from .models import Subject, TimeSlot, Semester
from .forms import SubjectForm, TimeSlotForm, SubjectWithTimeSlotsForm, SemesterForm, TimeSlotFormSet

class TimetableView(LoginRequiredMixin, TemplateView):
    """시간표 메인 뷰"""
    template_name = 'timetable/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # 현재 학기 가져오기
        current_semester = Semester.objects.filter(user=user, is_current=True).first()
        
        # 사용자의 모든 과목 가져오기
        subjects = Subject.objects.filter(user=user).prefetch_related('time_slots')
        
        # 시간표 데이터 구성
        timetable_data = {}
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        periods = range(1, 11)  # 1교시부터 10교시까지
        
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
            'current_semester': current_semester,
            'subjects': subjects,
            'timetable_data': timetable_data,
            'days': days,
            'periods': periods,
            'day_names': {
                'MON': '월',
                'TUE': '화',
                'WED': '수',
                'THU': '목',
                'FRI': '금',
                'SAT': '토'
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
        return Subject.objects.filter(user=self.request.user).prefetch_related('time_slots')

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    """과목 수정 뷰"""
    model = Subject
    form_class = SubjectForm
    template_name = 'timetable/subject_edit.html'
    success_url = reverse_lazy('timetable:index')
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['timeslot_formset'] = TimeSlotFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['timeslot_formset'] = TimeSlotFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        timeslot_formset = context['timeslot_formset']
        
        with transaction.atomic():
            if timeslot_formset.is_valid():
                self.object = form.save()
                timeslot_formset.instance = self.object
                timeslot_formset.save()
                messages.success(self.request, f'"{self.object.name}" 과목이 성공적으로 수정되었습니다.')
                return redirect(self.success_url)
            else:
                return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '과목 수정 중 오류가 발생했습니다.')
        return super().form_invalid(form)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    """과목 삭제 뷰"""
    model = Subject
    template_name = 'timetable/subject_delete.html'
    success_url = reverse_lazy('timetable:index')
    
    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)
    
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
