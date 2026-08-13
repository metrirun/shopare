import requests
import sys
import time

def check_url_accessibility(url):
    """
    بررسی دسترسی به یک URL
    Returns: True اگر قابل دسترس باشد، False در غیر این صورت
    """
    try:
        # استفاده از HEAD برای بررسی سریع
        response = requests.head(url, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            print(f'✅ لینک قابل مشاهده است (Status Code: 200)')
            print(f'📁 اندازه فایل: {response.headers.get("content-length", "نامشخص")} bytes')
            return True
        elif response.status_code == 404:
            print('❌ لینک پیدا نشد (Status Code: 404)')
            return False
        elif response.status_code == 403:
            print('🚫 دسترسی ممنوع (Status Code: 403)')
            return False
        else:
            print(f'⚠️ وضعیت نامشخص: {response.status_code}')
            return False
            
    except requests.exceptions.Timeout:
        print('⏱️ زمان درخواست به پایان رسید - لینک در دسترس نیست')
        return False
    except requests.exceptions.ConnectionError:
        print('🔴 خطای اتصال - لینک در دسترس نیست')
        return False
    except requests.exceptions.SSLError:
        print('🔒 خطای SSL - ممکن است لینک معتبر نباشد')
        return False
    except requests.exceptions.RequestException as e:
        print(f'❌ خطای درخواست: {e}')
        return False
    except Exception as e:
        print(f'❌ خطای ناشناخته: {e}')
        return False

def main():
    # URL مورد نظر برای بررسی
    url = 'http://45.147.76.237:9000/Data/Software/Metrica_Tracking.zip'
    
    print(f'🔍 در حال بررسی لینک: {url}')
    print('-' * 50)
    
    is_accessible = check_url_accessibility(url)
    
    # خروجی با کد مناسب برای GitHub Actions
    if is_accessible:
        print('✅ نتیجه: لینک قابل دسترس است')
        sys.exit(0)  # موفقیت
    else:
        print('❌ نتیجه: لینک قابل دسترس نیست')
        sys.exit(1)  # شکست

if __name__ == "__main__":
    main()
