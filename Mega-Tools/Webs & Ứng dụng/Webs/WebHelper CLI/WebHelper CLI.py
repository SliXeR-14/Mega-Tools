import os
import re
import sys
import webbrowser
import requests
from urllib.parse import urlparse
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(Fore.CYAN + Style.BRIGHT + "╔════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + "║          🌐 WebHelper CLI          ║")
    print(Fore.CYAN + Style.BRIGHT + "║   🛠️ Công cụ hỗ trợ Web cơ bản     ║")
    print(Fore.CYAN + Style.BRIGHT + "╠════════════════════════════════════╣")
    print(Fore.BLUE + Style.DIM    + "║   -----Powered by SliXeR-14-----   ║")
    print(Fore.BLUE + Style.DIM    + "║     © 2025 – copyright reversed    ║")
    print(Fore.CYAN + Style.BRIGHT + "╚════════════════════════════════════╝")

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        return "https://" + url
    return url

def check_status():
    url = input(Fore.YELLOW + "🔗 Nhập URL: ").strip()
    url = normalize_url(url)
    try:
        r = requests.head(url, allow_redirects=True, timeout=8)
        print(Fore.GREEN + f"✅ {url} → HTTP {r.status_code}")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi: {e}")

def get_title():
    url = input(Fore.YELLOW + "🔗 Nhập URL: ").strip()
    url = normalize_url(url)
    try:
        r = requests.get(url, timeout=8)
        m = re.search(r"<title[^>]*>(.*?)</title>", r.text, flags=re.IGNORECASE|re.DOTALL)
        title = m.group(1).strip() if m else "(không tìm thấy tiêu đề)"
        print(Fore.GREEN + f"📄 Tiêu đề: {title}")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi: {e}")

def download_page():
    url = input(Fore.YELLOW + "🔗 Nhập URL: ").strip()
    url = normalize_url(url)
    filename = input(Fore.CYAN + "💾 Tên file lưu (mặc định: index.html): ").strip() or "index.html"
    try:
        r = requests.get(url, timeout=15)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(Fore.GREEN + f"✅ Đã lưu {url} → {filename}")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi: {e}")

def open_browser():
    url = input(Fore.YELLOW + "🔗 Nhập URL: ").strip()
    url = normalize_url(url)
    try:
        webbrowser.open(url)
        print(Fore.GREEN + f"✅ Đã mở {url} trong trình duyệt")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi: {e}")

def main():
    while True:
        clear()
        banner()
        print(Fore.YELLOW + "\n📌 MENU CHỨC NĂNG")
        print(Fore.WHITE + "1. Kiểm tra trạng thái website (HEAD)")
        print("2. Lấy tiêu đề trang (HTML <title>)")
        print("3. Tải nội dung trang về file")
        print("4. Mở URL trong trình duyệt")
        print("0. Thoát")

        choice = input(Fore.CYAN + "\n👉 Chọn chức năng (0-4): ").strip()
        clear()
        banner()
        print()

        if choice == "1":
            check_status()
        elif choice == "2":
            get_title()
        elif choice == "3":
            download_page()
        elif choice == "4":
            open_browser()
        elif choice == "0":
            print(Fore.GREEN + "👋 Tạm biệt WebHelper CLI!")
            break
        else:
            print(Fore.RED + "⚠️ Lựa chọn không hợp lệ.")

        input(Fore.YELLOW + "\nNhấn Enter để quay lại menu...")

if __name__ == "__main__":
    main()
