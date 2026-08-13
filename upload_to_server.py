import json
import os
import sys
import requests
from pathlib import Path

def upload_json_to_server(file_path,server_url):
    """
    آپلود فایل JSON به سرور
    """
    try:
        # خواندن فایل JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f'📤 ارسال فایل به سرور: {server_url}')
        print(f'📁 نام فایل: {file_path}')
        print(f'📊 اندازه: {os.path.getsize(file_path)} bytes')
        
        # ارسال به سرور
        response = requests.post(
            f'{server_url}/upload-json',
            json=json_data,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print('✅ آپلود با موفقیت انجام شد')
            print(f'📨 پاسخ سرور: {response.json()}')
            return True
        else:
            print(f'❌ خطا در آپلود: {response.status_code}')
            print(f'پیام: {response.text}')
            return False
            
    except FileNotFoundError:
        print(f'❌ فایل {file_path} وجود ندارد')
        return False
    except json.JSONDecodeError as e:
        print(f'❌ خطا در خواندن JSON: {e}')
        return False
    except requests.exceptions.Timeout:
        print('⏱️ زمان درخواست به پایان رسید')
        return False
    except requests.exceptions.ConnectionError:
        print('🔴 خطای اتصال به سرور')
        return False
    except Exception as e:
        print(f'❌ خطای ناشناخته: {e}')
        return False

def upload_file_direct(file_path, server_url):
    """
    آپلود مستقیم فایل به سرور (روش جایگزین)
    """
    try:
        print(f'📤 ارسال فایل به عنوان فایل معمولی...')
        
        with open(file_path, 'rb') as f:
            files = {'files': (os.path.basename(file_path), f, 'application/json')}
            response = requests.post(
                f'{server_url}/upload-files',
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            print('✅ آپلود فایل با موفقیت انجام شد')
            print(f'📨 پاسخ: {response.json()}')
            return True
        else:
            print(f'❌ خطا: {response.status_code}')
            return False
            
    except Exception as e:
        print(f'❌ خطا: {e}')
        return False

def main():
    # تنظیمات
    SERVER_URL = 'http://45.147.76.237:8005'
    FILE_NAME = 'split_info_4.json'
    BRANCH = 'branch_part_26'
    
    print('=' * 60)
    print(f'📂 برنچ: {BRANCH}')
    print(f'📄 فایل: {FILE_NAME}')
    print('=' * 60)
    
    # بررسی وجود فایل
    if not os.path.exists(FILE_NAME):
        print(f'❌ فایل {FILE_NAME} در برنچ جاری وجود ندارد')
        sys.exit(1)
    
    print('✅ فایل وجود دارد')
    
    # روش 1: آپلود JSON
    print('\n🔄 روش 1: آپلود به عنوان JSON...')
    success1 = upload_json_to_server(FILE_NAME, SERVER_URL)
    
    # روش 2: آپلود فایل (اختیاری)
    print('\n🔄 روش 2: آپلود به عنوان فایل...')
    success2 = upload_file_direct(FILE_NAME, SERVER_URL)
    
    # نتیجه نهایی
    if success1 or success2:
        print('\n✅ حداقل یکی از روش‌های آپلود موفق بود')
        sys.exit(0)
    else:
        print('\n❌ تمام روش‌های آپلود ناموفق بودند')
        sys.exit(1)

if __name__ == '__main__':
    main()
