#!/usr/bin/env python3
"""
APK     
Android APK      .
"""

import zipfile
import struct
import os

def analyze_apk_structure(apk_path):
    """APK   """
    
    print(f"=== APK  : {apk_path} ===")
    
    if not os.path.exists(apk_path):
        print(" APK   .")
        return False
    
    file_size = os.path.getsize(apk_path)
    print(f"  : {file_size:,} bytes")
    
    try:
        with zipfile.ZipFile(apk_path, 'r') as apk:
            print("\n ZIP  :")
            print(" ZIP    ")
            
            #   
            file_list = apk.namelist()
            print(f"   : {len(file_list)}")
            
            #   
            required_files = [
                'AndroidManifest.xml',
                'classes.dex',
                'resources.arsc',
                'META-INF/MANIFEST.MF'
            ]
            
            print("\n   :")
            missing_files = []
            for required_file in required_files:
                if required_file in file_list:
                    file_info = apk.getinfo(required_file)
                    print(f" {required_file} ({file_info.file_size} bytes)")
                    
                    #   
                    if required_file == 'AndroidManifest.xml':
                        validate_manifest(apk, required_file)
                    elif required_file == 'classes.dex':
                        validate_dex(apk, required_file)
                    elif required_file == 'resources.arsc':
                        validate_resources(apk, required_file)
                        
                else:
                    print(f" {required_file} - ")
                    missing_files.append(required_file)
            
            if missing_files:
                print(f"\n   : {missing_files}")
                return False
            
            print("\n   :")
            for file_name in sorted(file_list):
                file_info = apk.getinfo(file_name)
                print(f"  - {file_name} ({file_info.file_size} bytes)")
            
            return True
            
    except zipfile.BadZipFile:
        print("  ZIP  ")
        return False
    except Exception as e:
        print(f" APK  : {e}")
        return False

def validate_manifest(apk, filename):
    """AndroidManifest.xml """
    try:
        content = apk.read(filename)
        
        #  XML  
        if len(content) < 8:
            print("     AndroidManifest.xml  ")
            return False
        
        # XML   
        magic = struct.unpack('<I', content[:4])[0]
        if magic == 0x00080003:
            print("      XML ")
        elif content.startswith(b'<?xml'):
            print("      XML  (  )")
        else:
            print(f"         (: 0x{magic:08x})")
            return False
        
        return True
        
    except Exception as e:
        print(f"     AndroidManifest.xml  : {e}")
        return False

def validate_dex(apk, filename):
    """classes.dex """
    try:
        content = apk.read(filename)
        
        if len(content) < 112:
            print("     DEX    ( 112 )")
            return False
        
        # DEX   
        if content[:4] != b'dex\n':
            print("     DEX   ")
            return False
        
        # DEX  
        version = content[4:8]
        if version not in [b'035\x00', b'037\x00', b'038\x00', b'039\x00']:
            print(f"        DEX : {version}")
        else:
            print(f"     DEX : {version.decode().strip()}")
        
        #   
        file_size = struct.unpack('<I', content[32:36])[0]
        if file_size != len(content):
            print(f"     DEX    (: {file_size}, : {len(content)})")
            return False
        
        print("     DEX    ")
        return True
        
    except Exception as e:
        print(f"     classes.dex  : {e}")
        return False

def validate_resources(apk, filename):
    """resources.arsc """
    try:
        content = apk.read(filename)
        
        if len(content) < 12:
            print("     resources.arsc  ")
            return False
        
        #    
        res_type = struct.unpack('<H', content[:2])[0]
        if res_type != 0x0002:
            print(f"        : 0x{res_type:04x}")
            return False
        
        print("     resources.arsc   ")
        return True
        
    except Exception as e:
        print(f"     resources.arsc  : {e}")
        return False

def get_apk_issues():
    """APK    """
    
    issues = [
        "1. AndroidManifest.xml   ",
        "2. classes.dex   ",
        "3. resources.arsc   ",
        "4.  META-INF   ",
        "5. ZIP    ",
        "6.  (alignment) ",
        "7.  SDK   ",
        "8.   "
    ]
    
    print("\n APK    :")
    for issue in issues:
        print(f"  {issue}")

def main():
    """  """
    
    apk_path = "downloads/planit-android.apk"
    
    print("APK     \n")
    
    # APK  
    is_valid = analyze_apk_structure(apk_path)
    
    #   
    get_apk_issues()
    
    if is_valid:
        print("\n APK   .")
        print("      (, ,  )")
    else:
        print("\n APK   .")
        print("        .")

if __name__ == "__main__":
    main()
