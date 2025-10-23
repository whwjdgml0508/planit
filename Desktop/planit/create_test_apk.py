#!/usr/bin/env python3
"""
간단한 테스트용 APK 생성 스크립트
실제로는 Android Studio나 React Native로 빌드해야 합니다.
"""

import zipfile
import os

def create_dummy_apk():
    """더미 APK 파일 생성 (테스트용)"""
    
    # APK는 실제로는 ZIP 파일 형식입니다
    apk_path = "downloads/planit-android.apk"
    
    # 기본 APK 구조 생성
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk:
        # AndroidManifest.xml (더미)
        manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.kafa.planit"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="PlanIt"
        android:theme="@style/AppTheme">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
        
        apk.writestr('AndroidManifest.xml', manifest_content)
        
        # classes.dex (더미)
        apk.writestr('classes.dex', b'dex\n035\x00' + b'\x00' * 100)
        
        # resources.arsc (더미)
        apk.writestr('resources.arsc', b'\x02\x00\x0C\x00' + b'\x00' * 50)
        
        # META-INF 폴더
        apk.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\n')
        apk.writestr('META-INF/CERT.SF', 'Signature-Version: 1.0\n')
        apk.writestr('META-INF/CERT.RSA', b'dummy certificate')
    
    print(f"✅ 테스트용 APK 생성 완료: {apk_path}")
    print(f"📁 파일 크기: {os.path.getsize(apk_path)} bytes")

if __name__ == "__main__":
    create_dummy_apk()
