# Script to remove app download and home screen buttons from production
$keyPath = "C:\Users\User\.ssh\ec2-kafa-2-key.pem"
$server = "ubuntu@35.163.12.109"

Write-Host "=== Removing Download and Install Buttons from Production ===" -ForegroundColor Cyan

# First, backup the current home.html
Write-Host "`nBacking up current home.html..." -ForegroundColor Yellow
ssh -i $keyPath $server "cp /home/ubuntu/planit/templates/home.html /home/ubuntu/planit/templates/home.html.backup"

# Create a new clean home.html without download/install buttons
Write-Host "`nCreating new home.html without download buttons..." -ForegroundColor Yellow

$newHomeHtml = @'
{% extends 'base.html' %}
{% load static %}

{% block title %}PlanIt - 생도 학습 관리 플랫폼{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="bg-primary text-white py-5 mb-5" style="border-radius: 0;">
    <div class="container py-4">
        <div class="row align-items-center">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <h1 class="display-4 fw-bold mb-4" style="font-size: 3.5rem; line-height: 1.1;">
                    <i class="fas fa-graduation-cap me-2"></i>PlanIt
                </h1>
                <p class="lead mb-4" style="font-size: 1.375rem; line-height: 1.5; font-weight: 400; opacity: 0.95;">
                    학습 데이터를 통합하고 학과 커뮤니티를 연계하여<br>
                    생도 생활의 효율성과 소통을 강화하는 웹사이트
                </p>
                {% if user.is_authenticated %}
                <div class="d-flex gap-3 flex-wrap">
                    <a href="{% url 'timetable:index' %}" class="btn btn-light btn-lg px-4">
                        <i class="fas fa-calendar-alt me-2"></i>시간표 보기
                    </a>
                    <a href="{% url 'planner:daily_planner' %}" class="btn btn-outline-light btn-lg px-4">
                        <i class="fas fa-tasks me-2"></i>플래너 보기
                    </a>
                </div>
                {% else %}
                <div class="d-flex gap-3 flex-wrap">
                    <a href="{% url 'accounts:register' %}" class="btn btn-light btn-lg px-4">
                        <i class="fas fa-user-plus me-2"></i>시작하기
                    </a>
                    <a href="{% url 'accounts:login' %}" class="btn btn-outline-light btn-lg px-4" target="_self">
                        <i class="fas fa-sign-in-alt me-2"></i>로그인
                    </a>
                </div>
                {% endif %}
            </div>
            <div class="col-lg-6 text-center">
                <i class="fas fa-laptop-code" style="font-size: 12rem; opacity: 0.2;"></i>
            </div>
        </div>
    </div>
</div>

<!-- Features Section -->
<div class="container mb-5 py-5">
    <div class="row text-center mb-5">
        <div class="col-12">
            <h2 class="fw-bold mb-3" style="font-size: 2.5rem; letter-spacing: -0.02em;">주요 기능</h2>
            <p class="text-muted" style="font-size: 1.125rem;">PlanIt이 제공하는 핵심 기능들을 확인해보세요</p>
        </div>
    </div>
    
    <div class="row g-4">
        <!-- 스터디 플래너 -->
        <div class="col-md-4">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body text-center p-5">
                    <div class="d-inline-flex align-items-center justify-content-center mb-4" style="width: 72px; height: 72px; background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%); border-radius: 18px;">
                        <i class="fas fa-calendar-check text-white" style="font-size: 2rem;"></i>
                    </div>
                    <h5 class="card-title fw-bold mb-3" style="font-size: 1.25rem;">스터디 플래너</h5>
                    <p class="card-text" style="color: #636366; font-size: 1rem; line-height: 1.6;">
                        수정 가능한 시간표와 각 과목별 평가 방식을 기록하고 학습 진도를 추적할 수 있습니다.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- 커뮤니티 -->
        <div class="col-md-4">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body text-center p-5">
                    <div class="d-inline-flex align-items-center justify-content-center mb-4" style="width: 72px; height: 72px; background: linear-gradient(135deg, #34C759 0%, #30D158 100%); border-radius: 18px;">
                        <i class="fas fa-users text-white" style="font-size: 2rem;"></i>
                    </div>
                    <h5 class="card-title fw-bold mb-3" style="font-size: 1.25rem;">커뮤니티</h5>
                    <p class="card-text" style="color: #636366; font-size: 1rem; line-height: 1.6;">
                        학과별 소통 공간에서 시험 자료를 공유하고 강의 특성 정보를 나눌 수 있습니다.
                    </p>
                </div>
            </div>
        </div>
        
        <!-- 통합 정보 관리 -->
        <div class="col-md-4">
            <div class="card h-100 shadow-sm border-0">
                <div class="card-body text-center p-5">
                    <div class="d-inline-flex align-items-center justify-content-center mb-4" style="width: 72px; height: 72px; background: linear-gradient(135deg, #AF52DE 0%, #FF2D55 100%); border-radius: 18px;">
                        <i class="fas fa-database text-white" style="font-size: 2rem;"></i>
                    </div>
                    <h5 class="card-title fw-bold mb-3" style="font-size: 1.25rem;">통합 정보 관리</h5>
                    <p class="card-text" style="color: #636366; font-size: 1rem; line-height: 1.6;">
                        E-class와 구글 클래스 정보를 통합하여 강의계획서와 평가 정보를 한 곳에서 관리합니다.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Call to Action -->
{% if not user.is_authenticated %}
<div class="container text-center py-5 my-5">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <h3 class="fw-bold mb-4" style="font-size: 2.25rem; letter-spacing: -0.02em;">지금 시작해보세요</h3>
            <p class="mb-5" style="color: #636366; font-size: 1.125rem; line-height: 1.6;">
                PlanIt과 함께 체계적인 학습 관리를 시작하고<br>
                동료들과 소통하며 함께 성장해보세요.
            </p>
            <a href="{% url 'accounts:register' %}" class="btn btn-primary btn-lg px-5">
                <i class="fas fa-rocket me-2"></i>무료로 시작하기
            </a>
        </div>
    </div>
</div>
{% endif %}
{% endblock %}
'@

# Write the new content to a temporary file
$tempFile = [System.IO.Path]::GetTempFileName()
$newHomeHtml | Out-File -FilePath $tempFile -Encoding UTF8

# Upload the new file to the server
Write-Host "`nUploading new home.html to server..." -ForegroundColor Yellow
scp -i $keyPath $tempFile "${server}:/tmp/new_home.html"

# Replace the old file with the new one
Write-Host "`nReplacing home.html on server..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo mv /tmp/new_home.html /home/ubuntu/planit/templates/home.html && sudo chown ubuntu:ubuntu /home/ubuntu/planit/templates/home.html"

# Clean up temp file
Remove-Item $tempFile

# Restart services
Write-Host "`nRestarting Django and Nginx services..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl restart planit && sudo systemctl restart nginx"

Write-Host "`n=== Waiting for services to restart ===" -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Check service status
Write-Host "`nChecking service status..." -ForegroundColor Yellow
ssh -i $keyPath $server "sudo systemctl status planit --no-pager -l | head -20"

Write-Host "`n=== Update Complete! ===" -ForegroundColor Green
Write-Host "Please check http://planit.boramae.club/ to verify the changes." -ForegroundColor Green
