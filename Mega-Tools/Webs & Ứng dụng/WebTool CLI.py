import os
import requests
import speedtest
import qrcode
from colorama import init, Fore, Back, Style

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
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"✅ Trạng thái: {response.status_code} – {response.reason}")
    except Exception as e:
        print(Fore.RED + f"❌ Không thể truy cập: {e}")

def generate_html_template():
    print(Fore.MAGENTA + "\n📄 Mã HTML mẫu:")
    print(Fore.WHITE + Style.DIM + """
<!DOCTYPE html>
<html>
<head>
    <title>Trang Web Mẫu</title>
    <style>
        body { font-family: sans-serif; background: #f0f0f0; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Chào mừng đến với WebTool CLI!</h1>
</body>
</html>
""")

def generate_qr():
    url = input(Fore.YELLOW + "🔗 Nhập URL để tạo mã QR: ")
    img = qrcode.make(url)
    img.save("qr_code.png")
    print(Fore.GREEN + "✅ Đã tạo mã QR và lưu vào file qr_code.png")

def test_speed():
    print(Fore.BLUE + "⏳ Đang kiểm tra tốc độ mạng...")
    st = speedtest.Speedtest()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000
    print(Fore.GREEN + f"📥 Tốc độ tải xuống: {download:.2f} Mbps")
    print(Fore.GREEN + f"📤 Tốc độ tải lên: {upload:.2f} Mbps")

def mock_api():
    print(Fore.CYAN + "📦 API giả lập:")
    print(Fore.WHITE + Style.DIM + """
GET /api/user
{
    "id": 1,
    "name": "Minh Dev",
    "email": "minh@example.com"
}
""")
