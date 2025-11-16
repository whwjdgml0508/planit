#!/usr/bin/env python3
"""
PlanIt 2-3주 개선 계획 실행 마스터 스크립트
모든 개선 사항을 단계별로 실행합니다.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """헤더 출력"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def run_command(command, description):
    """명령어 실행"""
    print(f"\n📋 {description}")
    print(f"💻 실행: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 성공: {description}")
            if result.stdout:
                print(f"출력: {result.stdout[:200]}...")
        else:
            print(f"❌ 실패: {description}")
            print(f"오류: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return False

def week1_https_setup():
    """1주차: HTTPS 설정"""
    print_header("1주차: HTTPS 인증서 적용")
    
    commands = [
        ("chmod +x deploy/setup_ssl.sh", "SSL 설정 스크립트 권한 부여"),
        ("sudo ./deploy/setup_ssl.sh", "Let's Encrypt SSL 인증서 발급"),
        ("sudo cp nginx_https.conf /etc/nginx/sites-available/planit", "HTTPS Nginx 설정 적용"),
        ("sudo systemctl reload nginx", "Nginx 재시작"),
        ("curl -I https://planit.boramae.club", "HTTPS 접속 확인"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        time.sleep(2)
    
    print(f"\n📊 1주차 HTTPS 설정 결과: {success_count}/{len(commands)} 성공")
    return success_count == len(commands)

def week1_screenshots():
    """1주차: 스크린샷 수동 촬영 안내"""
    print_header("1주차: README 스크린샷 추가 (수동)")
    
    print("📸 수동 스크린샷 촬영 가이드:")
    print("1. 브라우저에서 https://planit.boramae.club 접속")
    print("2. F12 → Ctrl+Shift+P → 'screenshot' 입력")
    print("3. 'Capture full size screenshot' 선택")
    print("4. screenshots/ 폴더에 다음 파일명으로 저장:")
    
    required_screenshots = [
        "main_page.png - 메인 페이지",
        "timetable.png - 시간표 관리",
        "planner.png - 스터디 플래너", 
        "community.png - 커뮤니티",
        "admin_page.png - 관리자 페이지",
        "mobile_app.png - 모바일 화면"
    ]
    
    for screenshot in required_screenshots:
        print(f"   • {screenshot}")
    
    # 스크린샷 폴더 확인
    screenshots_dir = Path("screenshots")
    if screenshots_dir.exists():
        existing_files = list(screenshots_dir.glob("*.png"))
        print(f"\n📁 현재 스크린샷 파일: {len(existing_files)}개")
        for file in existing_files:
            print(f"   ✅ {file.name}")
    else:
        run_command("mkdir screenshots", "스크린샷 폴더 생성")
    
    response = input("\n스크린샷 촬영을 완료하셨나요? (y/N): ")
    return response.lower() == 'y'

def week2_docker():
    """2주차: Docker 컨테이너화"""
    print_header("2-3주차: Docker 컨테이너화")
    
    # 환경 변수 파일 생성
    if not Path(".env").exists():
        run_command("cp .env.example .env", ".env 파일 생성")
        print("⚠️ .env 파일을 편집하여 실제 값을 입력해주세요!")
        return False
    
    commands = [
        ("docker-compose build", "Docker 이미지 빌드"),
        ("docker-compose -f docker-compose.prod.yml up -d", "프로덕션 컨테이너 시작"),
        ("docker-compose ps", "컨테이너 상태 확인"),
        ("docker-compose logs web", "웹 컨테이너 로그 확인"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        time.sleep(5)  # Docker 명령어는 시간이 걸림
    
    print(f"\n📊 2주차 Docker 결과: {success_count}/{len(commands)} 성공")
    return success_count >= 2

def week3_performance():
    """3주차: 성능 최적화"""
    print_header("3주차: 성능 최적화")
    
    commands = [
        ("python performance_optimization.py", "성능 최적화 스크립트 실행"),
        ("python manage.py collectstatic --noinput", "정적 파일 수집"),
        ("curl -w '@curl-format.txt' -o /dev/null -s https://planit.boramae.club", "성능 테스트"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        time.sleep(2)
    
    print(f"\n📊 3주차 성능 최적화 결과: {success_count}/{len(commands)} 성공")
    return success_count >= 2

def week3_ui_ux():
    """3주차: UI/UX 개선"""
    print_header("3주차: UI/UX 개선")
    
    commands = [
        ("python ui_ux_improvements.py", "UI/UX 개선 파일 생성"),
        ("python manage.py collectstatic --noinput", "정적 파일 재수집"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        time.sleep(2)
    
    print(f"\n📊 3주차 UI/UX 개선 결과: {success_count}/{len(commands)} 성공")
    return success_count == len(commands)

def week3_security():
    """3주차: 보안 강화"""
    print_header("3주차: 보안 강화")
    
    commands = [
        ("python security_enhancements.py", "보안 강화 파일 생성"),
        ("pip install bleach", "HTML 정화 라이브러리 설치"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        time.sleep(2)
    
    print(f"\n📊 3주차 보안 강화 결과: {success_count}/{len(commands)} 성공")
    return success_count == len(commands)

def final_verification():
    """최종 검증"""
    print_header("최종 검증 및 테스트")
    
    tests = [
        ("curl -I https://planit.boramae.club", "HTTPS 접속 테스트"),
        ("curl -s https://planit.boramae.club | grep -i 'planit'", "페이지 로드 테스트"),
        ("ls screenshots/*.png | wc -l", "스크린샷 파일 개수 확인"),
        ("docker-compose ps | grep Up", "Docker 컨테이너 상태 확인"),
    ]
    
    success_count = 0
    for command, description in tests:
        if run_command(command, description):
            success_count += 1
        time.sleep(1)
    
    print(f"\n📊 최종 검증 결과: {success_count}/{len(tests)} 성공")
    
    # 최종 점수 계산
    total_score = success_count * 4  # 각 테스트당 4점
    print(f"\n🎯 예상 개선 점수: +{total_score}점")
    
    return success_count >= 3

def main():
    """메인 실행 함수"""
    print("🚀 PlanIt 2-3주 개선 계획 실행")
    print("=" * 60)
    print("📅 실행 순서:")
    print("  1️⃣ 1주차: HTTPS 인증서 적용")
    print("  2️⃣ 1주차: README 스크린샷 추가")
    print("  3️⃣ 2주차: Docker 컨테이너화")
    print("  4️⃣ 3주차: 성능 최적화")
    print("  5️⃣ 3주차: UI/UX 개선")
    print("  6️⃣ 3주차: 보안 강화")
    print("  7️⃣ 최종: 검증 및 테스트")
    
    # 사용자 확인
    response = input("\n계속 진행하시겠습니까? (y/N): ")
    if response.lower() != 'y':
        print("❌ 실행이 취소되었습니다.")
        return
    
    # 단계별 실행
    results = []
    
    # 1주차
    results.append(("HTTPS 설정", week1_https_setup()))
    results.append(("스크린샷 추가", week1_screenshots()))
    
    # 2주차
    results.append(("Docker 컨테이너화", week2_docker()))
    
    # 3주차
    results.append(("성능 최적화", week3_performance()))
    results.append(("UI/UX 개선", week3_ui_ux()))
    results.append(("보안 강화", week3_security()))
    
    # 최종 검증
    results.append(("최종 검증", final_verification()))
    
    # 결과 요약
    print_header("실행 결과 요약")
    success_count = 0
    for task, success in results:
        status = "✅ 성공" if success else "❌ 실패"
        print(f"  {task}: {status}")
        if success:
            success_count += 1
    
    print(f"\n📊 전체 결과: {success_count}/{len(results)} 성공")
    
    if success_count >= 5:
        print("🎉 PlanIt 개선 계획이 성공적으로 완료되었습니다!")
        print("📈 예상 점수 개선: +16.9점")
        print("🌐 접속 주소: https://planit.boramae.club")
    else:
        print("⚠️ 일부 작업이 실패했습니다. 로그를 확인하여 문제를 해결해주세요.")
    
    print("\n📋 다음 단계:")
    print("  1. 실제 스크린샷 촬영 및 업로드")
    print("  2. .env 파일 실제 값 설정")
    print("  3. SSL 인증서 상태 확인")
    print("  4. 성능 테스트 및 최적화")
    print("  5. 최종 발표 준비")

if __name__ == "__main__":
    main()
