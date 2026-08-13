import requests
import sys
import os
import subprocess
from datetime import datetime

def download_file(url, local_filename):
    """
    دانلود فایل از URL
    """
    try:
        print(f'📥 شروع دانلود: {local_filename}')
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # دریافت اندازه فایل
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(local_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    # نمایش پیشرفت دانلود
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        #print(f'📊 پیشرفت: {percent:.1f}%', end='\r')
        
        print(f'\n✅ دانلود کامل شد: {local_filename}')
        print(f'📁 حجم فایل: {downloaded:,} bytes')
        return True
        
    except requests.exceptions.Timeout:
        print('⏱️ زمان دانلود به پایان رسید')
        return False
    except requests.exceptions.ConnectionError:
        print('🔴 خطای اتصال در حین دانلود')
        return False
    except requests.exceptions.HTTPError as e:
        print(f'❌ خطای HTTP: {e}')
        return False
    except Exception as e:
        print(f'❌ خطا در دانلود: {e}')
        return False

def check_and_download():
    """
    بررسی دسترسی و دانلود فایل
    """
    url = 'http://45.147.76.237:9000/Data/Software/Metrica_Tracking.zip'
    local_filename = 'Metrica_Tracking.zip'
    
    print(f'🔍 بررسی لینک: {url}')
    print('-' * 60)
    
    # مرحله 1: بررسی دسترسی
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            print(f'❌ لینک در دسترس نیست (Status: {response.status_code})')
            return False
            
        print('✅ لینک قابل دسترس است')
        print(f'📁 اندازه فایل: {response.headers.get("content-length", "نامشخص")} bytes')
        print('-' * 60)
        
    except Exception as e:
        print(f'❌ خطا در بررسی لینک: {e}')
        return False
    
    # مرحله 2: دانلود فایل
    print('🔄 شروع دانلود...')
    if not download_file(url, local_filename):
        return False
    
    # مرحله 3: بررسی فایل دانلود شده
    if os.path.exists(local_filename):
        file_size = os.path.getsize(local_filename)
        print(f'✅ فایل با موفقیت ذخیره شد: {local_filename} ({file_size:,} bytes)')
        return True
    else:
        print('❌ فایل ذخیره نشد')
        return False

def git_commit_and_push():
    """
    Commit و Push فایل به ریپو
    """
    try:
        # تنظیم Git
        os.environ['GIT_AUTHOR_NAME'] = 'GitHub Action'
        os.environ['GIT_AUTHOR_EMAIL'] = 'action@github.com'
        os.environ['GIT_COMMITTER_NAME'] = 'GitHub Action'
        os.environ['GIT_COMMITTER_EMAIL'] = 'action@github.com'
        
        # Add فایل
        subprocess.run(['git', 'add', 'Metrica_Tracking.zip'], check=True)
        
        # Commit با پیام
        commit_message = f'Download Metrica_Tracking.zip on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push
        subprocess.run(['git', 'push'], check=True)
        
        print('✅ فایل با موفقیت به ریپو اضافه و Push شد')
        return True
        
    except subprocess.CalledProcessError as e:
        print(f'❌ خطا در Git: {e}')
        return False
    except Exception as e:
        print(f'❌ خطای ناشناخته در Git: {e}')
        return False

def main():
    # دانلود فایل
    if check_and_download():
        # Commit و Push
        print('-' * 60)
        print('🔄 در حال افزودن فایل به ریپو...')
        if git_commit_and_push():
            print('✅ عملیات با موفقیت انجام شد')
            sys.exit(0)
        else:
            print('❌ خطا در Commit/Push')
            sys.exit(1)
    else:
        print('❌ دانلود ناموفق بود')
        sys.exit(1)

if __name__ == "__main__":
    main()
