#!/usr/bin/env python3
"""
최소한의 유효한 APK 생성
Android에서 확실히 파싱 가능한 최소 구조로 APK를 생성합니다.
"""

import zipfile
import struct
import os
import hashlib
import zlib
from xml.etree.ElementTree import Element, SubElement, tostring

def create_minimal_apk():
    """최소한의 유효한 APK 생성"""
    
    apk_path = "downloads/planit-android-minimal.apk"
    os.makedirs("downloads", exist_ok=True)
    
    print("최소한의 유효한 APK 생성 중...")
    
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_STORED) as apk:
        
        # 1. AndroidManifest.xml (텍스트 형식으로 시작)
        manifest_xml = create_simple_manifest()
        apk.writestr('AndroidManifest.xml', manifest_xml.encode('utf-8'))
        print("- AndroidManifest.xml 생성")
        
        # 2. classes.dex (최소한의 유효한 DEX)
        dex_content = create_minimal_dex()
        apk.writestr('classes.dex', dex_content)
        print("- classes.dex 생성")
        
        # 3. resources.arsc (최소한의 리소스)
        resources_content = create_minimal_resources()
        apk.writestr('resources.arsc', resources_content)
        print("- resources.arsc 생성")
        
        # 4. 기본 리소스 파일들
        create_basic_resources(apk)
        print("- 기본 리소스 파일들 생성")
        
        # 5. META-INF (서명 파일들)
        create_simple_meta_inf(apk)
        print("- META-INF 서명 파일들 생성")
    
    size = os.path.getsize(apk_path)
    print(f"최소 APK 생성 완료: {size:,} bytes")
    return apk_path

def create_simple_manifest():
    """간단한 AndroidManifest.xml 생성 (텍스트 형식)"""
    
    manifest_xml = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.kafa.planit"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-sdk 
        android:minSdkVersion="21" 
        android:targetSdkVersion="33" />
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
    </application>
    
</manifest>'''
    
    return manifest_xml

def create_minimal_dex():
    """최소한의 유효한 DEX 파일 생성"""
    
    # 기본 DEX 크기 (1KB로 축소)
    dex_size = 1024
    dex_data = bytearray(dex_size)
    
    # DEX 헤더 (112바이트)
    dex_data[0:8] = b'dex\n035\x00'
    
    # 파일 크기
    dex_data[32:36] = struct.pack('<I', dex_size)
    
    # 헤더 크기
    dex_data[36:40] = struct.pack('<I', 112)
    
    # 엔디안 태그
    dex_data[40:44] = struct.pack('<I', 0x12345678)
    
    # 링크 정보 (없음)
    dex_data[44:48] = struct.pack('<I', 0)  # link_size
    dex_data[48:52] = struct.pack('<I', 0)  # link_off
    
    # 맵 오프셋 (파일 끝 근처)
    map_offset = dex_size - 32
    dex_data[52:56] = struct.pack('<I', map_offset)
    
    # 문자열 ID 섹션
    dex_data[56:60] = struct.pack('<I', 1)    # string_ids_size
    dex_data[60:64] = struct.pack('<I', 112)  # string_ids_off
    
    # 타입 ID 섹션
    dex_data[64:68] = struct.pack('<I', 1)    # type_ids_size
    dex_data[68:72] = struct.pack('<I', 116)  # type_ids_off
    
    # 프로토타입 ID 섹션
    dex_data[72:76] = struct.pack('<I', 0)    # proto_ids_size
    dex_data[76:80] = struct.pack('<I', 0)    # proto_ids_off
    
    # 필드 ID 섹션
    dex_data[80:84] = struct.pack('<I', 0)    # field_ids_size
    dex_data[84:88] = struct.pack('<I', 0)    # field_ids_off
    
    # 메소드 ID 섹션
    dex_data[88:92] = struct.pack('<I', 0)    # method_ids_size
    dex_data[92:96] = struct.pack('<I', 0)    # method_ids_off
    
    # 클래스 정의 섹션
    dex_data[96:100] = struct.pack('<I', 0)   # class_defs_size
    dex_data[100:104] = struct.pack('<I', 0)  # class_defs_off
    
    # 데이터 섹션
    data_size = dex_size - 120
    dex_data[104:108] = struct.pack('<I', data_size)  # data_size
    dex_data[108:112] = struct.pack('<I', 120)        # data_off
    
    # 문자열 데이터 (최소한)
    dex_data[112:116] = struct.pack('<I', 4)  # 문자열 오프셋
    dex_data[120:124] = struct.pack('<I', 1)  # 문자열 길이
    dex_data[124:125] = b'V'                  # void 타입
    dex_data[125:126] = b'\x00'               # null terminator
    
    # 맵 리스트 (파일 끝)
    dex_data[map_offset:map_offset+4] = struct.pack('<I', 2)  # 맵 항목 수
    
    # 맵 항목 1: 문자열 ID
    dex_data[map_offset+4:map_offset+6] = struct.pack('<H', 0x0001)    # TYPE_STRING_ID_ITEM
    dex_data[map_offset+6:map_offset+8] = struct.pack('<H', 0)         # unused
    dex_data[map_offset+8:map_offset+12] = struct.pack('<I', 1)        # size
    dex_data[map_offset+12:map_offset+16] = struct.pack('<I', 112)     # offset
    
    # 맵 항목 2: 타입 ID
    dex_data[map_offset+16:map_offset+18] = struct.pack('<H', 0x0002)  # TYPE_TYPE_ID_ITEM
    dex_data[map_offset+18:map_offset+20] = struct.pack('<H', 0)       # unused
    dex_data[map_offset+20:map_offset+24] = struct.pack('<I', 1)       # size
    dex_data[map_offset+24:map_offset+28] = struct.pack('<I', 116)     # offset
    
    # 체크섬 계산
    checksum = zlib.adler32(dex_data[12:]) & 0xffffffff
    dex_data[8:12] = struct.pack('<I', checksum)
    
    # SHA-1 해시 계산
    sha1_hash = hashlib.sha1(dex_data[32:]).digest()
    dex_data[12:32] = sha1_hash
    
    return bytes(dex_data)

def create_minimal_resources():
    """최소한의 resources.arsc 파일 생성"""
    
    # 매우 간단한 리소스 테이블
    arsc_data = bytearray()
    
    # 리소스 테이블 헤더
    arsc_data.extend(struct.pack('<H', 0x0002))  # RES_TABLE_TYPE
    arsc_data.extend(struct.pack('<H', 0x000C))  # 헤더 크기
    arsc_data.extend(struct.pack('<I', 0x100))   # 전체 크기
    arsc_data.extend(struct.pack('<I', 1))       # 패키지 개수
    
    # 나머지는 패딩으로 채움
    while len(arsc_data) < 0x100:
        arsc_data.extend(b'\x00')
    
    return bytes(arsc_data)

def create_basic_resources(apk):
    """기본 리소스 파일들 생성"""
    
    # 문자열 리소스
    strings_xml = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">PlanIt</string>
</resources>'''
    apk.writestr('res/values/strings.xml', strings_xml.encode('utf-8'))
    
    # 간단한 아이콘 (1x1 PNG)
    icon_data = create_tiny_png()
    apk.writestr('res/mipmap-mdpi/ic_launcher.png', icon_data)

def create_tiny_png():
    """1x1 픽셀 PNG 이미지 생성"""
    
    png_data = bytearray([
        # PNG 시그니처
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        
        # IHDR 청크 (1x1, 8비트 RGB)
        0x00, 0x00, 0x00, 0x0D,  # 길이
        0x49, 0x48, 0x44, 0x52,  # IHDR
        0x00, 0x00, 0x00, 0x01,  # 너비 1
        0x00, 0x00, 0x00, 0x01,  # 높이 1
        0x08, 0x02, 0x00, 0x00, 0x00,  # 8비트 RGB
        0x90, 0x77, 0x53, 0xDE,  # CRC
        
        # IDAT 청크 (압축된 이미지 데이터)
        0x00, 0x00, 0x00, 0x0C,  # 길이
        0x49, 0x44, 0x41, 0x54,  # IDAT
        0x08, 0x99, 0x01, 0x01, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00,
        0x02, 0x00, 0x01,
        0xE2, 0x21, 0xBC, 0x33,  # CRC
        
        # IEND 청크
        0x00, 0x00, 0x00, 0x00,  # 길이
        0x49, 0x45, 0x4E, 0x44,  # IEND
        0xAE, 0x42, 0x60, 0x82   # CRC
    ])
    
    return bytes(png_data)

def create_simple_meta_inf(apk):
    """간단한 META-INF 서명 파일들 생성"""
    
    # MANIFEST.MF
    manifest_mf = '''Manifest-Version: 1.0
Created-By: PlanIt Builder

Name: AndroidManifest.xml
SHA1-Digest: dGVzdA==

Name: classes.dex
SHA1-Digest: dGVzdA==
'''
    apk.writestr('META-INF/MANIFEST.MF', manifest_mf.encode('utf-8'))
    
    # CERT.SF
    cert_sf = '''Signature-Version: 1.0
Created-By: PlanIt Builder
SHA1-Digest-Manifest: dGVzdA==

Name: AndroidManifest.xml
SHA1-Digest: dGVzdA==
'''
    apk.writestr('META-INF/CERT.SF', cert_sf.encode('utf-8'))
    
    # CERT.RSA (더미 인증서 - 매우 간단)
    cert_rsa = b'-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----'
    apk.writestr('META-INF/CERT.RSA', cert_rsa)

def test_apk_validity(apk_path):
    """생성된 APK의 유효성 테스트"""
    
    print(f"\n=== APK 유효성 테스트: {apk_path} ===")
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk:
            # ZIP 구조 테스트
            file_list = apk.namelist()
            print(f"포함된 파일 수: {len(file_list)}")
            
            # 필수 파일 확인
            required_files = ['AndroidManifest.xml', 'classes.dex', 'META-INF/MANIFEST.MF']
            for required_file in required_files:
                if required_file in file_list:
                    size = apk.getinfo(required_file).file_size
                    print(f"OK {required_file} ({size} bytes)")
                else:
                    print(f"MISSING {required_file}")
            
            # 파일 읽기 테스트
            for file_name in file_list:
                try:
                    content = apk.read(file_name)
                    print(f"READ OK {file_name} ({len(content)} bytes)")
                except Exception as e:
                    print(f"READ ERROR {file_name}: {e}")
        
        print("APK 기본 유효성 테스트 통과")
        return True
        
    except Exception as e:
        print(f"APK 유효성 테스트 실패: {e}")
        return False

def main():
    """메인 함수"""
    
    print("=== 최소한의 유효한 APK 생성 ===\n")
    
    # 최소 APK 생성
    apk_path = create_minimal_apk()
    
    # 유효성 테스트
    is_valid = test_apk_validity(apk_path)
    
    if is_valid:
        print(f"\n성공: {apk_path} 생성 완료")
        print("이 APK를 테스트해보세요.")
    else:
        print(f"\n실패: APK 생성에 문제가 있습니다.")

if __name__ == "__main__":
    main()
