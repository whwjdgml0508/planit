#!/usr/bin/env python3
"""
PlanIt UI/UX 개선 스크립트
반응형 디자인, 접근성, 사용자 경험을 개선합니다.
"""

import os
from pathlib import Path

def create_responsive_css():
    """반응형 CSS 개선"""
    css_content = """
/* PlanIt 반응형 디자인 개선 */

/* 모바일 우선 접근법 */
.container-fluid {
    padding: 0 15px;
}

/* 태블릿 (768px 이상) */
@media (min-width: 768px) {
    .container-fluid {
        padding: 0 30px;
    }
    
    .timetable-grid {
        font-size: 0.9rem;
    }
}

/* 데스크톱 (992px 이상) */
@media (min-width: 992px) {
    .container-fluid {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .sidebar {
        position: sticky;
        top: 20px;
    }
}

/* 대형 화면 (1200px 이상) */
@media (min-width: 1200px) {
    .main-content {
        display: grid;
        grid-template-columns: 250px 1fr;
        gap: 30px;
    }
}

/* 접근성 개선 */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* 포커스 표시 개선 */
.btn:focus,
.form-control:focus,
.nav-link:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

/* 고대비 모드 지원 */
@media (prefers-contrast: high) {
    .card {
        border: 2px solid #000;
    }
    
    .btn-primary {
        background-color: #000;
        border-color: #000;
    }
}

/* 다크 모드 지원 */
@media (prefers-color-scheme: dark) {
    :root {
        --bs-body-bg: #121212;
        --bs-body-color: #ffffff;
        --bs-card-bg: #1e1e1e;
    }
    
    .card {
        background-color: var(--bs-card-bg);
        color: var(--bs-body-color);
    }
}

/* 애니메이션 감소 설정 */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* 터치 친화적 버튼 크기 */
@media (pointer: coarse) {
    .btn {
        min-height: 44px;
        min-width: 44px;
    }
    
    .nav-link {
        padding: 12px 16px;
    }
}
"""
    
    css_file = Path("static/css/responsive.css")
    css_file.parent.mkdir(parents=True, exist_ok=True)
    css_file.write_text(css_content, encoding='utf-8')
    print(f"✅ 반응형 CSS 생성: {css_file}")

def create_accessibility_js():
    """접근성 JavaScript"""
    js_content = """
// PlanIt 접근성 개선 스크립트

document.addEventListener('DOMContentLoaded', function() {
    // 1. 키보드 네비게이션 개선
    setupKeyboardNavigation();
    
    // 2. ARIA 라벨 자동 추가
    setupAriaLabels();
    
    // 3. 포커스 관리
    setupFocusManagement();
    
    // 4. 스크린 리더 지원
    setupScreenReaderSupport();
});

function setupKeyboardNavigation() {
    // ESC 키로 모달 닫기
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance.hide();
            }
        }
    });
    
    // Tab 키 순환 개선
    const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const focusable = modal.querySelectorAll(focusableElements);
            if (focusable.length > 0) {
                focusable[0].focus();
            }
        });
    });
}

function setupAriaLabels() {
    // 버튼에 ARIA 라벨 추가
    document.querySelectorAll('button:not([aria-label])').forEach(btn => {
        if (btn.textContent.trim()) {
            btn.setAttribute('aria-label', btn.textContent.trim());
        }
    });
    
    // 폼 필드에 설명 추가
    document.querySelectorAll('input, select, textarea').forEach(field => {
        const label = document.querySelector(`label[for="${field.id}"]`);
        if (label && !field.getAttribute('aria-describedby')) {
            const helpText = field.parentNode.querySelector('.form-text');
            if (helpText) {
                const helpId = field.id + '-help';
                helpText.id = helpId;
                field.setAttribute('aria-describedby', helpId);
            }
        }
    });
}

function setupFocusManagement() {
    // 페이지 로드 시 메인 콘텐츠로 포커스 이동
    const mainContent = document.querySelector('main, #main-content, .main-content');
    if (mainContent && !mainContent.getAttribute('tabindex')) {
        mainContent.setAttribute('tabindex', '-1');
        mainContent.focus();
    }
    
    // 스킵 링크 추가
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = '메인 콘텐츠로 건너뛰기';
    skipLink.className = 'sr-only sr-only-focusable';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        z-index: 1000;
        padding: 8px 16px;
        background: #007bff;
        color: white;
        text-decoration: none;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

function setupScreenReaderSupport() {
    // 동적 콘텐츠 변경 알림
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    announcer.id = 'announcer';
    document.body.appendChild(announcer);
    
    // 전역 알림 함수
    window.announceToScreenReader = function(message) {
        announcer.textContent = message;
        setTimeout(() => {
            announcer.textContent = '';
        }, 1000);
    };
    
    // AJAX 요청 완료 시 알림
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        return originalFetch.apply(this, args).then(response => {
            if (response.ok) {
                announceToScreenReader('페이지 내용이 업데이트되었습니다.');
            }
            return response;
        });
    };
}

// 다크 모드 토글
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    announceToScreenReader(isDark ? '다크 모드가 활성화되었습니다.' : '라이트 모드가 활성화되었습니다.');
}

// 저장된 다크 모드 설정 복원
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// 폰트 크기 조절
function adjustFontSize(direction) {
    const root = document.documentElement;
    const currentSize = parseFloat(getComputedStyle(root).fontSize);
    const newSize = direction === 'increase' ? currentSize + 2 : currentSize - 2;
    
    if (newSize >= 12 && newSize <= 24) {
        root.style.fontSize = newSize + 'px';
        localStorage.setItem('fontSize', newSize);
        announceToScreenReader(`폰트 크기가 ${newSize}px로 변경되었습니다.`);
    }
}

// 저장된 폰트 크기 복원
const savedFontSize = localStorage.getItem('fontSize');
if (savedFontSize) {
    document.documentElement.style.fontSize = savedFontSize + 'px';
}
"""
    
    js_file = Path("static/js/accessibility.js")
    js_file.parent.mkdir(parents=True, exist_ok=True)
    js_file.write_text(js_content, encoding='utf-8')
    print(f"✅ 접근성 JavaScript 생성: {js_file}")

def create_accessibility_toolbar():
    """접근성 도구모음 HTML"""
    html_content = """
<!-- 접근성 도구모음 -->
<div class="accessibility-toolbar" id="accessibility-toolbar">
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="toggleDarkMode()" 
            aria-label="다크 모드 토글">
        🌙 다크모드
    </button>
    
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="adjustFontSize('increase')"
            aria-label="폰트 크기 증가">
        A+
    </button>
    
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="adjustFontSize('decrease')"
            aria-label="폰트 크기 감소">
        A-
    </button>
    
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="toggleHighContrast()"
            aria-label="고대비 모드 토글">
        🔲 고대비
    </button>
</div>

<style>
.accessibility-toolbar {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 1050;
    background: rgba(255, 255, 255, 0.9);
    padding: 5px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.accessibility-toolbar .btn {
    margin: 0 2px;
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    .accessibility-toolbar {
        position: relative;
        top: auto;
        right: auto;
        margin-bottom: 10px;
        text-align: center;
    }
}
</style>
"""
    
    html_file = Path("templates/includes/accessibility_toolbar.html")
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.write_text(html_content, encoding='utf-8')
    print(f"✅ 접근성 도구모음 HTML 생성: {html_file}")

if __name__ == "__main__":
    print("🎨 PlanIt UI/UX 개선 도구")
    print("=" * 50)
    
    # 1. 반응형 CSS 생성
    create_responsive_css()
    
    # 2. 접근성 JavaScript 생성
    create_accessibility_js()
    
    # 3. 접근성 도구모음 생성
    create_accessibility_toolbar()
    
    print("\n🎉 UI/UX 개선 파일 생성 완료!")
    print("📋 추가 작업:")
    print("  1. base.html에 CSS/JS 파일 포함")
    print("  2. 접근성 도구모음 템플릿 포함")
    print("  3. 색상 대비 검사 및 조정")
    print("  4. 키보드 네비게이션 테스트")
