# 🌐 NetHelper CLI — Ultra Deluxe

NetHelper CLI là một công cụ dòng lệnh viết bằng **C++** giúp kiểm tra và hỗ trợ các tác vụ liên quan đến web và mạng.  
Ứng dụng có giao diện CLI với hiệu ứng ASCII, màu sắc và nhiều chức năng tiện ích.

---

## ✨ Tính năng chính
- 🔎 Kiểm tra trạng thái HTTP (status code)
- 📄 Lấy tiêu đề trang web (`<title>`)
- 📑 Xem HTTP headers
- 💾 Tải HTML về file
- 🔑 Sinh mật khẩu ngẫu nhiên
- ⏱️ Đo thời gian phản hồi HTTP
- 🖧 Ping website
- 🔒 Kiểm tra SSL certificate
- 🌍 DNS Lookup & Reverse DNS
- 🧭 Traceroute
- 🛡️ Quét cổng (Port Scanner)
- 📝 Trích xuất meta info (charset, description)
- 📬 Thử HTTP methods (GET/POST/HEAD/OPTIONS)
- 🎨 Đổi theme (Hacker, Cyberpunk, Retro)
- 🟢 Matrix Mode (hiệu ứng ma trận)

---

## ⚙️ Yêu cầu hệ thống

### Windows
- **Visual Studio 2019/2022** (hoặc compiler hỗ trợ C++17 trở lên)
- **libcurl** (Windows build: [https://curl.se/windows/](https://curl.se/windows/))
- Thư viện **Ws2_32.lib** (có sẵn trong Windows SDK)

### Linux / macOS
- Compiler hỗ trợ **C++17** (g++, clang++)
- **libcurl** (`sudo apt install libcurl4-openssl-dev` trên Ubuntu/Debian)
- Các thư viện hệ thống: `pthread`, `dl`, `rt` (thường có sẵn)

---

## 🚀 Cách build

### Trên Linux / macOS
g++ -std=c++17 NetHelper.cpp -o nethelper -lcurl -lpthread

### Trên Windows (Visual Studio)
Mở project .vcxproj trong Visual Studio

Thêm đường dẫn include/lib của libcurl

Link thêm libcurl.lib và Ws2_32.lib

---

## ▶️ Cách chạy
./nethelper

Sau đó chọn chức năng từ menu (0–16).

---

## 📂 Cấu trúc repo
NetHelper-CLI/

│── NetHelper.cpp        # Source code chính

│── NetHelper.vcxproj    # File project Visual Studio

│── README.md            # Hướng dẫn sử dụng

---

## 📜 Giấy phép
Dự án được phát triển bởi SliXeR-14 (2025). 

Bạn có thể sử dụng, chỉnh sửa và phân phối lại theo nhu cầu cá nhân.

---

## 📦 Thư viện cần cài
- **libcurl** (ngoài chuẩn, bắt buộc)
- **Winsock2 (Ws2_32.lib)** (Windows, có sẵn trong SDK)
- Các thư viện chuẩn C++ (iostream, string, regex, fstream, chrono, thread, vector, sstream, random) → đã có sẵn trong compiler.

---
