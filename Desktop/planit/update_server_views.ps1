# 서버에서 직접 views.py 파일 수정
$EC2_IP = "35.163.12.109"
$EC2_USER = "ubuntu"
$SSH_KEY_PATH = "C:\Users\User\ssh\ec2-kafa-2-key.pem"

Write-Host "서버에서 직접 views.py 파일을 수정합니다..." -ForegroundColor Blue

# 1. 기존 Django 프로세스 종료
Write-Host "1. 기존 Django 프로세스 종료..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "pkill -f 'python manage.py runserver'"

# 2. views.py 파일 수정
Write-Host "2. views.py 파일 수정..." -ForegroundColor Yellow
$viewsContent = @'
    def form_invalid(self, form):
        # 디버깅을 위한 구체적인 오류 메시지 추가
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        
        if error_messages:
            messages.error(self.request, f'과목 수정 중 오류가 발생했습니다: {", ".join(error_messages)}')
        else:
            messages.error(self.request, '과목 수정 중 오류가 발생했습니다. 입력 내용을 확인해주세요.')
        return super().form_invalid(form)
'@

# 기존 form_invalid 메서드를 새로운 것으로 교체
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && sed -i '/def form_invalid(self, form):/,/return super().form_invalid(form)/c\
    def form_invalid(self, form):\
        # 디버깅을 위한 구체적인 오류 메시지 추가\
        error_messages = []\
        for field, errors in form.errors.items():\
            for error in errors:\
                error_messages.append(f\"{field}: {error}\")\
        \
        if error_messages:\
            messages.error(self.request, f\"과목 수정 중 오류가 발생했습니다: {\", \".join(error_messages)}\")\
        else:\
            messages.error(self.request, \"과목 수정 중 오류가 발생했습니다. 입력 내용을 확인해주세요.\")\
        return super().form_invalid(form)' timetable/views.py"

# 3. Django 개발 서버 재시작
Write-Host "3. Django 개발 서버 재시작..." -ForegroundColor Yellow
ssh -i $SSH_KEY_PATH $EC2_USER@$EC2_IP "cd /var/www/planit && source venv/bin/activate && nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &"

Write-Host "`n✅ 서버 파일 수정이 완료되었습니다!" -ForegroundColor Green
Write-Host "🌐 사이트에서 과목 색상 변경을 시도해보세요: http://planit.boramae.club/" -ForegroundColor Cyan
Write-Host "📋 이제 구체적인 오류 메시지가 표시됩니다." -ForegroundColor Yellow
