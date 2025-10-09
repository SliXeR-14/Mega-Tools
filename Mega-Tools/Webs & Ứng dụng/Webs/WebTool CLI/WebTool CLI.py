import os
import requests
import speedtest
import qrcode
import time
from colorama import init, Fore, Style

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(Fore.CYAN + Style.BRIGHT + "╔════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + "║         🌐 WebTool CLI             ║")
    print(Fore.CYAN + Style.BRIGHT + "║   Công cụ hỗ trợ Web & App Dev     ║")
    print(Fore.CYAN + Style.BRIGHT + "╠════════════════════════════════════╣")
    print(Fore.LIGHTBLUE_EX + Style.DIM    + "║     Powered by SliXeR-14           ║")
    print(Fore.LIGHTBLUE_EX + Style.DIM    + "║     © 2025 – All rights reserved   ║")
    print(Fore.CYAN + Style.BRIGHT + "╚════════════════════════════════════╝")

def check_website():
    url = input(Fore.YELLOW + "🔗 Nhập URL website (vd: https://google.com): ")
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "WebToolCLI/1.0"})
        print(Fore.GREEN + f"✅ Trạng thái: {response.status_code} – {response.reason}")
    except Exception as e:
        print(Fore.RED + f"❌ Không thể truy cập: {e}")

# 🔥 UPDATE: Ping website (HTTP latency)
def ping_website():
    url = input(Fore.YELLOW + "🔗 Nhập URL website để ping (vd: https://google.com): ")
    try:
        start = time.time()
        response = requests.get(url, timeout=5, headers={"User-Agent": "WebToolCLI/1.0"})
        latency = (time.time() - start) * 1000
        print(Fore.GREEN + f"✅ Ping thành công: {latency:.2f} ms – Status {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"❌ Ping thất bại: {e}")

def generate_html_template():
    html_code = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Trang Web Mẫu</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root { --bg: #f0f0f0; --fg: #333; --card: #fff; --border: #ddd; }
        body { margin: 0; font-family: system-ui, sans-serif; background: var(--bg); color: var(--fg); }
        .container { max-width: 800px; margin: 4rem auto; padding: 2rem; background: var(--card); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
        h1 { margin-top: 0; font-weight: 700; }
        p { line-height: 1.6; }
        .btn { display: inline-block; padding: .6rem 1rem; border-radius: 8px; border: 1px solid var(--border); background: #fafafa; text-decoration: none; color: inherit; }
        .btn:hover { background: #f3f3f3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chào mừng đến với WebTool CLI!</h1>
        <p>Bạn có thể dùng mẫu này để bắt đầu nhanh một dự án frontend nhỏ.</p>
        <a class="btn" href="#">Bắt đầu</a>
    </div>
</body>
</html>"""
    print(Fore.MAGENTA + "\n📄 Mã HTML mẫu:")
    print(Fore.WHITE + Style.DIM + html_code)

    # 🔥 UPDATE: cho phép lưu ra file
    save = input(Fore.CYAN + "\n💾 Bạn có muốn lưu file HTML này? (y/n): ")
    if save.lower() == "y":
        filename = input(Fore.YELLOW + "Nhập tên file (mặc định: template.html): ") or "template.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_code)
        print(Fore.GREEN + f"✅ Đã lưu file {filename}")

def generate_qr():
    url = input(Fore.YELLOW + "🔗 Nhập URL để tạo mã QR: ")
    filename = input(Fore.CYAN + "💾 Nhập tên file để lưu (mặc định: qr_code.png): ") or "qr_code.png"
    try:
        img = qrcode.make(url)
        img.save(filename)
        print(Fore.GREEN + f"✅ Đã tạo mã QR và lưu vào file {filename}")
    except Exception as e:
        print(Fore.RED + f"❌ Tạo QR thất bại: {e}")

def test_speed():
    print(Fore.BLUE + "⏳ Đang kiểm tra tốc độ mạng...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        best = st.get_best_server()
        print(Fore.CYAN + f"🌍 Server: {best['sponsor']} ({best['name']}, {best['country']})")
        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        print(Fore.GREEN + f"📥 Tốc độ tải xuống: {download:.2f} Mbps")
        print(Fore.GREEN + f"📤 Tốc độ tải lên: {upload:.2f} Mbps")
    except Exception as e:
        print(Fore.RED + f"❌ Không thể kiểm tra tốc độ mạng: {e}")

def mock_api():
    print(Fore.CYAN + "📦 API giả lập:")
    print(Fore.WHITE + Style.DIM + """
GET /api/user
{
    "id": your id,
    "name": "your name",
    "email": "yourname.example.com"
}
""")

def main():
    while True:
        clear()
        banner()
        print(Fore.YELLOW + "\n📌 MENU CHỨC NĂNG")
        print(Fore.WHITE + "1. Kiểm tra website")
        print("2. Ping website (HTTP latency)")  # 🔥 UPDATE
        print("3. Tạo mã HTML mẫu")
        print("4. Tạo mã QR từ URL")
        print("5. Kiểm tra tốc độ mạng")
        print("6. API giả lập")
        print("0. Thoát")
        choice = input(Fore.CYAN + "\n👉 Chọn chức năng (0-6): ")

        clear()
        banner()
        print()
        if choice == "1":
            check_website()
        elif choice == "2":
            ping_website()
        elif choice == "3":
            generate_html_template()
        elif choice == "4":
            generate_qr()
        elif choice == "5":
            test_speed()
        elif choice == "6":
            mock_api()
        elif choice == "0":
            print(Fore.GREEN + "👋 Tạm biệt WebTool CLI!")
            break
        else:
            print(Fore.RED + "⚠️ Lựa chọn không hợp lệ.")

        input(Fore.YELLOW + "\nNhấn Enter để quay lại menu...")

if __name__ == "__main__":
    main()
