"""
PWA 아이콘 생성 스크립트
Pillow 라이브러리를 사용하여 다양한 크기의 PNG 아이콘 생성
"""
import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow 라이브러리가 필요합니다. 설치 중...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont

# 아이콘 크기 목록
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# 출력 디렉토리
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'icons')

def create_icon(size):
    """지정된 크기의 아이콘 생성"""
    # 새 이미지 생성 (RGBA)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 배경 그라디언트 효과 (단순화: 단색 사용)
    # 둥근 모서리 사각형 그리기
    corner_radius = size // 5
    
    # 배경색 (Bootstrap primary blue)
    bg_color = (13, 110, 253)  # #0d6efd
    
    # 둥근 사각형 그리기
    draw.rounded_rectangle(
        [(0, 0), (size-1, size-1)],
        radius=corner_radius,
        fill=bg_color
    )
    
    # "P" 글자 그리기
    font_size = int(size * 0.55)
    try:
        # 시스템 폰트 사용 시도
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except:
            # 기본 폰트 사용
            font = ImageFont.load_default()
    
    text = "P"
    # 텍스트 위치 계산
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - size // 20
    
    draw.text((x, y), text, fill='white', font=font)
    
    # 작은 원 (플러스 아이콘 배경)
    circle_radius = size // 10
    circle_x = size - circle_radius * 2 - size // 10
    circle_y = size // 10
    
    # 노란색 원
    draw.ellipse(
        [(circle_x, circle_y), (circle_x + circle_radius * 2, circle_y + circle_radius * 2)],
        fill=(255, 193, 7)  # #ffc107
    )
    
    # 플러스 기호
    plus_color = 'white'
    line_width = max(2, size // 50)
    center_x = circle_x + circle_radius
    center_y = circle_y + circle_radius
    plus_size = circle_radius * 0.6
    
    # 가로선
    draw.line(
        [(center_x - plus_size, center_y), (center_x + plus_size, center_y)],
        fill=plus_color, width=line_width
    )
    # 세로선
    draw.line(
        [(center_x, center_y - plus_size), (center_x, center_y + plus_size)],
        fill=plus_color, width=line_width
    )
    
    return img

def main():
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("PlanIt PWA 아이콘 생성 중...")
    
    for size in ICON_SIZES:
        icon = create_icon(size)
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        icon.save(filepath, 'PNG')
        print(f"  ✓ {filename} 생성 완료")
    
    # 추가 아이콘 생성
    # favicon
    favicon = create_icon(32)
    favicon.save(os.path.join(OUTPUT_DIR, 'favicon-32x32.png'), 'PNG')
    print("  ✓ favicon-32x32.png 생성 완료")
    
    favicon16 = create_icon(16)
    favicon16.save(os.path.join(OUTPUT_DIR, 'favicon-16x16.png'), 'PNG')
    print("  ✓ favicon-16x16.png 생성 완료")
    
    # Apple touch icon
    apple_icon = create_icon(180)
    apple_icon.save(os.path.join(OUTPUT_DIR, 'apple-touch-icon.png'), 'PNG')
    print("  ✓ apple-touch-icon.png 생성 완료")
    
    print("\n모든 아이콘 생성 완료!")
    print(f"출력 위치: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
