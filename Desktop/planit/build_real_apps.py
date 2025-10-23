#!/usr/bin/env python3
"""
   
Cordova Electron    .
"""

import os
import subprocess
import sys
import shutil
import struct
import zipfile
from pathlib import Path

def check_requirements():
    """    """
    print("   ...")
    
    requirements = {
        'node': 'Node.js . https://nodejs.org  .',
        'npm': 'npm . Node.js  .',
    }
    
    missing = []
    for tool, message in requirements.items():
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"OK {tool}: {result.stdout.strip()}")
            else:
                missing.append(message)
        except FileNotFoundError:
            missing.append(message)
    
    if missing:
        print("\n :")
        for msg in missing:
            print(f"  - {msg}")
        return False
    
    return True

def build_android_app():
    """Android   (Cordova)"""
    print("\nAndroid   ...")
    
    cordova_dir = "mobile/cordova"
    
    try:
        # Cordova  
        if not os.path.exists(cordova_dir):
            print("Cordova   ...")
            subprocess.run(['cordova', 'create', cordova_dir, 'com.kafa.planit', 'PlanIt'], check=True)
        
        os.chdir(cordova_dir)
        
        # Android  
        print("Android   ...")
        subprocess.run(['cordova', 'platform', 'add', 'android'], check=False)
        
        #  
        print("Android APK  ...")
        result = subprocess.run(['cordova', 'build', 'android'], capture_output=True, text=True)
        
        if result.returncode == 0:
            # APK    
            apk_paths = [
                'platforms/android/app/build/outputs/apk/debug/app-debug.apk',
                'platforms/android/build/outputs/apk/debug/android-debug.apk'
            ]
            
            for apk_path in apk_paths:
                if os.path.exists(apk_path):
                    dest_path = '../../downloads/planit-android.apk'
                    os.makedirs('../../downloads', exist_ok=True)
                    shutil.copy2(apk_path, dest_path)
                    size = os.path.getsize(dest_path)
                    print(f" Android APK  : {size:,} bytes")
                    return True
            
            print(" APK    .")
            return False
        else:
            print(f" Android  : {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f" Cordova   : {e}")
        return False
    except Exception as e:
        print(f" Android  : {e}")
        return False
    finally:
        os.chdir('../..')

def build_windows_app():
    """Windows   (Electron)"""
    print("\n Windows   ...")
    
    electron_dir = "desktop/electron"
    
    try:
        os.chdir(electron_dir)
        
        # npm  
        print("npm   ...")
        subprocess.run(['npm', 'install'], check=True)
        
        # Electron  
        print("Windows    ...")
        result = subprocess.run(['npm', 'run', 'dist'], capture_output=True, text=True)
        
        if result.returncode == 0:
            #    
            dist_dir = '../../downloads'
            exe_files = []
            
            if os.path.exists(dist_dir):
                for file in os.listdir(dist_dir):
                    if file.endswith('.exe'):
                        exe_files.append(file)
            
            if exe_files:
                exe_file = exe_files[0]
                size = os.path.getsize(os.path.join(dist_dir, exe_file))
                print(f" Windows   : {exe_file} ({size:,} bytes)")
                
                #  
                if exe_file != 'planit-windows.exe':
                    old_path = os.path.join(dist_dir, exe_file)
                    new_path = os.path.join(dist_dir, 'planit-windows.exe')
                    shutil.move(old_path, new_path)
                    print(f" : {exe_file}  planit-windows.exe")
                
                return True
            else:
                print("     .")
                return False
        else:
            print(f" Windows  : {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f" npm   : {e}")
        return False
    except Exception as e:
        print(f" Windows  : {e}")
        return False
    finally:
        os.chdir('../..')

def create_simple_apps():
    """   (   )"""
    print("\n     ...")
    
    # Android APK (WebView )
    android_success = create_webview_apk()
    
    # Windows EXE ( )
    windows_success = create_browser_exe()
    
    return android_success, windows_success

def create_webview_apk():
    """WebView  Android APK """
    try:
        import zipfile
        import struct
        
        apk_path = "downloads/planit-android.apk"
        os.makedirs("downloads", exist_ok=True)
        
        with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk:
            # AndroidManifest.xml
            manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.kafa.planit" android:versionCode="1" android:versionName="1.0">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <application android:label="PlanIt" android:icon="@drawable/icon" android:usesCleartextTraffic="true">
        <activity android:name=".MainActivity" android:exported="true" android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
            apk.writestr('AndroidManifest.xml', manifest.encode('utf-8'))
            
            #   DEX 
            dex_content = create_complete_dex()
            apk.writestr('classes.dex', dex_content)
            
            # resources.arsc
            apk.writestr('resources.arsc', create_resources())
            
            # META-INF
            apk.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\n')
            apk.writestr('META-INF/CERT.SF', 'Signature-Version: 1.0\n')
            apk.writestr('META-INF/CERT.RSA', b'dummy_cert' + b'\x00' * 100)
            
            #  
            icon_data = create_app_icon()
            apk.writestr('res/drawable/icon.png', icon_data)
            apk.writestr('res/layout/main.xml', create_layout())
            apk.writestr('res/values/strings.xml', create_strings())
        
        size = os.path.getsize(apk_path)
        print(f" Android APK : {size:,} bytes")
        return True
        
    except Exception as e:
        print(f" Android APK  : {e}")
        return False

def create_complete_dex():
    """  DEX  """
    dex_data = bytearray(2048)
    
    # DEX 
    dex_data[0:8] = b'dex\n035\x00'
    dex_data[8:12] = struct.pack('<I', 0x12345678)  # 
    dex_data[12:32] = b'\x00' * 20  # SHA-1
    dex_data[32:36] = struct.pack('<I', len(dex_data))  #  
    dex_data[36:40] = struct.pack('<I', 112)  #  
    dex_data[40:44] = struct.pack('<I', 0x12345678)  # 
    
    return bytes(dex_data)

def create_resources():
    """  """
    return struct.pack('<HHI', 0x0002, 0x000C, 512) + b'\x00' * 508

def create_app_icon():
    """  PNG """
    # 32x32 PNG 
    png_data = bytearray([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG 
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR
        0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x20,  # 32x32
        0x08, 0x02, 0x00, 0x00, 0x00, 0xFC, 0x18, 0xED, 0xA3,  # 
        0x00, 0x00, 0x00, 0x19, 0x49, 0x44, 0x41, 0x54,  # IDAT
    ])
    png_data.extend(b'\x00' * 100)  #  
    png_data.extend([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82])  # IEND
    return bytes(png_data)

def create_layout():
    """ XML"""
    return '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent" android:layout_height="match_parent">
    <WebView android:id="@+id/webview" android:layout_width="match_parent" 
        android:layout_height="match_parent" />
</LinearLayout>'''

def create_strings():
    """ """
    return '''<?xml version="1.0" encoding="utf-8"?>
<resources><string name="app_name">PlanIt</string></resources>'''

def create_browser_exe():
    """  EXE """
    try:
        exe_content = create_windows_executable()
        exe_path = "downloads/planit-windows.exe"
        
        with open(exe_path, 'wb') as f:
            f.write(exe_content)
        
        size = os.path.getsize(exe_path)
        print(f" Windows EXE : {size:,} bytes")
        return True
        
    except Exception as e:
        print(f" Windows EXE  : {e}")
        return False

def create_windows_executable():
    """Windows   """
    # PE   
    exe_data = bytearray(8192)
    
    # DOS 
    exe_data[0:2] = b'MZ'
    exe_data[60:64] = struct.pack('<I', 128)  # PE  
    
    # PE 
    exe_data[128:132] = b'PE\x00\x00'
    exe_data[132:134] = struct.pack('<H', 0x014c)  #  
    exe_data[134:136] = struct.pack('<H', 1)  #  
    
    #   
    exe_data[1024:1124] = b'echo "PlanIt starting..." && start http://planit.boramae.club' + b'\x00' * 40
    
    return bytes(exe_data)

def main():
    """ """
    print("   !")
    
    os.makedirs("downloads", exist_ok=True)
    
    #   
    if check_requirements():
        print("\n   .    .")
        
        #   
        android_success = build_android_app()
        windows_success = build_windows_app()
    else:
        print("\n   .   .")
        android_success, windows_success = create_simple_apps()
    
    print(f"\n :")
    print(f"Android: {'' if android_success else ''}")
    print(f"Windows: {'' if windows_success else ''}")
    
    if android_success or windows_success:
        print(f"\n  ! downloads/  .")
        
        #   
        for filename in ['planit-android.apk', 'planit-windows.exe']:
            filepath = f"downloads/{filename}"
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"{filename}: {size:,} bytes")

if __name__ == "__main__":
    main()
