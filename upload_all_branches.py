import os
import subprocess
import requests
import sys
from pathlib import Path

SERVER_URL = "http://45.147.76.237:8005"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {"files": (os.path.basename(file_path), f)}
            response = requests.post(f"{SERVER_URL}/upload-files", files=files, timeout=30)
            return response.status_code == 200
    except Exception as e:
        print(f"    ❌ خطا: {e}")
        return False

def main():
    # دریافت لیست برنچ‌ها
    result = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True)
    branches = []
    for line in result.stdout.split("\n"):
        if "origin/" in line and "->" not in line:
            branch = line.strip().replace("origin/", "")
            branches.append(branch)

    print(f"📋 تعداد برنچ‌ها: {len(branches)}")
    print("=" * 60)

    total_success = 0
    total_fail = 0

    for i, branch in enumerate(branches, 1):
        print(f"\n🌿 [{i}/{len(branches)}] پردازش برنچ: {branch}")
        print("-" * 40)
        
        # چک‌اوت برنچ
        subprocess.run(["git", "checkout", branch], capture_output=True, text=True)
        
        # پیدا کردن فایل‌ها
        files = []
        for root, dirs, filenames in os.walk("."):
            if ".git" in root:
                continue
            for filename in filenames:
                if filename == ".git":
                    continue
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    files.append(file_path)
        
        if not files:
            print("  ℹ️ هیچ فایلی یافت نشد")
            continue
        
        branch_success = 0
        branch_fail = 0
        
        for file_path in files:
            try:
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    continue
                if file_size > MAX_FILE_SIZE:
                    print(f"  ⚠️ {file_path} - حجم بالا ({file_size} bytes) - رد شد")
                    continue
                
                print(f"  📤 آپلود: {file_path} ({file_size} bytes)")
                if upload_file(file_path):
                    print(f"    ✅ موفق")
                    branch_success += 1
                    total_success += 1
                else:
                    print(f"    ❌ ناموفق")
                    branch_fail += 1
                    total_fail += 1
            except Exception as e:
                print(f"  ❌ خطا در پردازش {file_path}: {e}")
                branch_fail += 1
                total_fail += 1
        
        print(f"  📊 خلاصه: ✅ {branch_success} | ❌ {branch_fail}")

    print("\n" + "=" * 60)
    print("📊 گزارش نهایی:")
    print(f"  ✅ آپلود موفق: {total_success}")
    print(f"  ❌ آپلود ناموفق: {total_fail}")
    print("=" * 60)

    # ذخیره گزارش
    with open("upload_report.txt", "w") as f:
        f.write("📊 گزارش آپلود\n")
        f.write("=" * 40 + "\n")
        f.write(f"کل برنچ‌ها: {len(branches)}\n")
        f.write(f"آپلود موفق: {total_success}\n")
        f.write(f"آپلود ناموفق: {total_fail}\n")
        f.write("\nلیست برنچ‌های پردازش شده:\n")
        for branch in branches:
            f.write(f"  - {branch}\n")

if __name__ == "__main__":
    main()
