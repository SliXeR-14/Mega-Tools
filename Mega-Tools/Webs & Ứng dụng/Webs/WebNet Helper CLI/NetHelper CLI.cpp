#include <iostream>
#include <string>
#include <curl/curl.h>
#include <regex>
#include <fstream>
#include <random>
#include <chrono>
#include <thread>
#include <vector>
#include <sstream>

#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <errno.h>
#endif

#define RESET   "\033[0m"
#define BLACK   "\033[30m"
#define RED     "\033[31m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define BLUE    "\033[34m"
#define MAGENTA "\033[35m"
#define CYAN    "\033[36m"
#define WHITE   "\033[37m"
#define BOLD    "\033[1m"

enum class Theme { Hacker, Cyberpunk, Retro };
struct Palette {
    std::string primary, accent, warn, ok, info;
};
Palette getPalette(Theme t) {
    switch (t) {
    case Theme::Hacker:    return { GREEN, CYAN, YELLOW, GREEN, WHITE };
    case Theme::Cyberpunk: return { MAGENTA, CYAN, YELLOW, GREEN, WHITE };
    case Theme::Retro:     return { BLUE, CYAN, YELLOW, GREEN, WHITE };
    default:               return { CYAN, WHITE, YELLOW, GREEN, WHITE };
    }
}
Theme CURRENT_THEME = Theme::Hacker;

const std::vector<std::string> USER_AGENTS = {
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
};

std::string randomUserAgent() {
    static std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<> dist(0, (int)USER_AGENTS.size() - 1);
    return USER_AGENTS[dist(gen)];
}

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void typeEffect(const std::string& text, int delayMs = 25, bool newline = true) {
    for (char c : text) {
        std::cout << c << std::flush;
        std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
    }
    if (newline) std::cout << "\n";
}

void spinner(const std::string& msg, int durationMs = 2000, const std::string& color = CYAN) {
    const char* spin = "|/-\\";
    auto start = std::chrono::steady_clock::now();
    int i = 0;
    while (std::chrono::steady_clock::now() - start < std::chrono::milliseconds(durationMs)) {
        std::cout << "\r" << color << msg << " " << spin[i++ % 4] << RESET << std::flush;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    std::cout << "\r" << msg << " ✅" << std::string(10, ' ') << "\n";
}

void loadingBar(int length = 30, int ms = 30, const std::string& color = CYAN) {
    std::cout << color << "[";
    for (int i = 0; i < length; i++) {
        std::cout << "#";
        std::cout.flush();
        std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    }
    std::cout << "]" << RESET << "\n";
}

void matrixRain(int lines = 12, int delay = 60, int width = 60) {
    std::srand((unsigned)std::time(nullptr));
    for (int i = 0; i < lines; i++) {
        for (int j = 0; j < width; j++) {
            int r = std::rand() % 2;
            if (r) std::cout << GREEN << "1" << RESET;
            else   std::cout << CYAN << "0" << RESET;
        }
        std::cout << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(delay));
    }
}

void asciiLogo() {
    std::string color = getPalette(CURRENT_THEME).primary;
    std::cout << color << R"(
 _   _      _   _      _   _      _   _ 
| \ | | ___| |_| |__  | | | | ___| |_| |
|  \| |/ _ \ __| '_ \ | |_| |/ _ \ __| |
| |\  |  __/ |_| | | ||  _  |  __/ |_|_|
|_| \_|\___|\__|_| |_||_| |_|\___|\__(_)
    )" << RESET << "\n";
}

void banner() {
    auto p = getPalette(CURRENT_THEME);
    std::cout << p.primary << "╔══════════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║              🌐 " << BOLD << "NetHelper CLI" << RESET << p.primary << "                                        ║\n";
    std::cout << "║      🛠️  Công cụ hỗ trợ Web (C++)                                    ║\n";
    std::cout << "╠══════════════════════════════════════════════════════════════════════╣\n";
    std::cout << "║      ----- Powered by SliXeR-14 -----                                ║\n";
    std::cout << "║      © 2025 – copyright reversed                                     ║\n";
    std::cout << "╚══════════════════════════════════════════════════════════════════════╝" << RESET << "\n";
}

void showThemeMenu() {
    auto p = getPalette(CURRENT_THEME);
    std::cout << "\n" << BOLD << "🎨 Chọn theme:" << RESET << "\n";
    std::cout << p.primary << "╔══════════════════════════════════╗\n";
    std::cout << "║ 1. 👨‍💻 Hacker (xanh lá)           ║\n";
    std::cout << "║ 2. 🤖 Cyberpunk (hồng tím)       ║\n";
    std::cout << "║ 3. 💎 Retro (xanh dương)         ║\n";
    std::cout << "╚══════════════════════════════════╝" << RESET << "\n";
}

size_t WriteToString(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}
size_t WriteToFile(void* contents, size_t size, size_t nmemb, void* userp) {
    std::ofstream* ofs = static_cast<std::ofstream*>(userp);
    ofs->write(static_cast<char*>(contents), size * nmemb);
    return size * nmemb;
}

std::string stripProtocol(const std::string& url) {
    if (url.rfind("http://", 0) == 0) return url.substr(7);
    if (url.rfind("https://", 0) == 0) return url.substr(8);
    return url;
}

void checkStatus(const std::string& url, const std::string& ua) {
    spinner("Đang kiểm tra trạng thái", 1200, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    long http_code = 0;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
        std::cout << GREEN << "✅ Trạng thái: HTTP " << http_code << RESET << "\n";
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void getTitle(const std::string& url, const std::string& ua) {
    spinner("Đang tải nội dung trang", 1200, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    std::string readBuffer;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteToString);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        std::regex title_regex("<title>(.*?)</title>", std::regex::icase);
        std::smatch match;
        if (std::regex_search(readBuffer, match, title_regex)) {
            std::cout << BLUE << "📄 Tiêu đề: " << match[1] << RESET << "\n";
        }
        else {
            std::cout << YELLOW << "⚠️ Không tìm thấy <title>" << RESET << "\n";
        }
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void showHeaders(const std::string& url, const std::string& ua) {
    spinner("Đang lấy headers", 1000, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    curl_easy_setopt(curl, CURLOPT_HEADER, 1L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void downloadHTML(const std::string& url, const std::string& ua, const std::string& filename = "downloaded.html") {
    spinner("Đang tải HTML", 1200, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    std::ofstream ofs(filename, std::ios::binary);
    if (!ofs) { std::cout << RED << "❌ Không thể mở file để ghi" << RESET << "\n"; curl_easy_cleanup(curl); return; }
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteToFile);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &ofs);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    ofs.close();
    if (res == CURLE_OK) {
        std::cout << GREEN << "✅ Đã tải HTML về file " << filename << RESET << "\n";
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void extractMetaInfo(const std::string& url, const std::string& ua) {
    spinner("Đang lấy meta info", 1000, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    std::string body;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteToString);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &body);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        std::smatch m;
        std::regex charset_re("<meta[^>]*charset=\\s*\"?([^\"]+)\"?", std::regex::icase);
        std::regex desc_re("<meta[^>]*name=\\s*\"description\"[^>]*content=\\s*\"([^\"]*)\"", std::regex::icase);
        if (std::regex_search(body, m, charset_re)) {
            std::cout << CYAN << "🧩 Charset: " << m[1] << RESET << "\n";
        }
        else {
            std::cout << YELLOW << "⚠️ Không tìm thấy charset" << RESET << "\n";
        }
        if (std::regex_search(body, m, desc_re)) {
            std::cout << CYAN << "📝 Description: " << m[1] << RESET << "\n";
        }
        else {
            std::cout << YELLOW << "⚠️ Không tìm thấy meta description" << RESET << "\n";
        }
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void httpMethodTest(const std::string& url, const std::string& method, const std::string& ua) {
    spinner("Đang thử HTTP method", 1000, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, method.c_str());
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    long code = 0;
    if (res == CURLE_OK) {
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &code);
        std::cout << GREEN << "✅ " << method << " → HTTP " << code << RESET << "\n";
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void measureLatency(const std::string& url, const std::string& ua) {
    spinner("Đang đo thời gian phản hồi", 1000, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    double total_time = 0;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        curl_easy_getinfo(curl, CURLINFO_TOTAL_TIME, &total_time);
        std::cout << GREEN << "⏱️ Thời gian phản hồi: " << (total_time * 1000) << " ms" << RESET << "\n";
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void checkSSL(const std::string& url, const std::string& ua) {
    spinner("Đang kiểm tra SSL certificate", 1200, getPalette(CURRENT_THEME).accent);
    CURL* curl = curl_easy_init();
    if (!curl) { std::cout << RED << "❌ Không khởi tạo được CURL" << RESET << "\n"; return; }
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1L);
    curl_easy_setopt(curl, CURLOPT_USERAGENT, ua.c_str());
    curl_easy_setopt(curl, CURLOPT_CERTINFO, 1L);
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        struct curl_certinfo* ci = nullptr;
        curl_easy_getinfo(curl, CURLINFO_CERTINFO, &ci);
        if (ci && ci->num_of_certs > 0) {
            std::cout << BLUE << "🔒 Thông tin chứng chỉ (" << ci->num_of_certs << "):" << RESET << "\n";
            for (int i = 0; i < ci->num_of_certs; ++i) {
                struct curl_slist* slist = ci->certinfo[i];
                while (slist) {
                    std::cout << CYAN << "• " << slist->data << RESET << "\n";
                    slist = slist->next;
                }
                if (i < ci->num_of_certs - 1) std::cout << "------------------------------------------------------------\n";
            }
        }
        else {
            std::cout << YELLOW << "⚠️ Không lấy được thông tin chứng chỉ (có thể không phải HTTPS)." << RESET << "\n";
        }
    }
    else {
        std::cout << RED << "❌ Lỗi: " << curl_easy_strerror(res) << RESET << "\n";
    }
    curl_easy_cleanup(curl);
}

void pingSite(const std::string& host) {
    spinner("Đang ping", 800, getPalette(CURRENT_THEME).accent);
#ifdef _WIN32
    std::string cmd = "ping -n 4 " + host;
#else
    std::string cmd = "ping -c 4 " + host;
#endif
    system(cmd.c_str());
}

void traceroute(const std::string& host) {
    spinner("Đang traceroute", 800, getPalette(CURRENT_THEME).accent);
#ifdef _WIN32
    std::string cmd = "tracert " + host;
#else
    std::string cmd = "traceroute " + host;
#endif
    system(cmd.c_str());
}

void dnsLookup(const std::string& domain) {
    spinner("Đang tra DNS", 800, getPalette(CURRENT_THEME).accent);
    addrinfo hints{}, * res;
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    int status = getaddrinfo(domain.c_str(), nullptr, &hints, &res);
    if (status != 0) {
#ifdef _WIN32
        std::cout << RED << "❌ Lỗi: " << WSAGetLastError() << RESET << "\n";
#else
        std::cout << RED << "❌ Lỗi: " << gai_strerror(status) << RESET << "\n";
#endif
        return;
    }
    std::cout << GREEN << "✅ IP cho " << domain << ":" << RESET << "\n";
    for (addrinfo* p = res; p != nullptr; p = p->ai_next) {
        char ipstr[INET6_ADDRSTRLEN];
        void* addr = nullptr;
        if (p->ai_family == AF_INET) {
            sockaddr_in* ipv4 = (sockaddr_in*)p->ai_addr;
            addr = &(ipv4->sin_addr);
        }
        else if (p->ai_family == AF_INET6) {
            sockaddr_in6* ipv6 = (sockaddr_in6*)p->ai_addr;
            addr = &(ipv6->sin6_addr);
        }
        if (addr) {
            inet_ntop(p->ai_family, addr, ipstr, sizeof(ipstr));
            std::cout << CYAN << "• " << ipstr << RESET << "\n";
        }
    }
    freeaddrinfo(res);
}

void reverseDNS(const std::string& ip) {
    spinner("Đang reverse DNS", 800, getPalette(CURRENT_THEME).accent);
    sockaddr_storage ss{};
    int family = (ip.find(':') != std::string::npos) ? AF_INET6 : AF_INET;
    if (family == AF_INET) {
        sockaddr_in sa{}; sa.sin_family = AF_INET;
        inet_pton(AF_INET, ip.c_str(), &(sa.sin_addr));
        memcpy(&ss, &sa, sizeof(sa));
    }
    else {
        sockaddr_in6 sa6{}; sa6.sin6_family = AF_INET6;
        inet_pton(AF_INET6, ip.c_str(), &(sa6.sin6_addr));
        memcpy(&ss, &sa6, sizeof(sa6));
    }
    char host[NI_MAXHOST];
    int r = getnameinfo((sockaddr*)&ss, (family == AF_INET ? sizeof(sockaddr_in) : sizeof(sockaddr_in6)),
        host, sizeof(host), nullptr, 0, NI_NAMEREQD);
    if (r == 0) {
        std::cout << GREEN << "✅ Domain: " << host << RESET << "\n";
    }
    else {
        std::cout << YELLOW << "⚠️ Không phân giải được reverse DNS" << RESET << "\n";
    }
}

bool tryConnect(const std::string& host, int port, int timeoutMs = 800) {
#ifdef _WIN32
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) return false;
    sockaddr_in addr{}; addr.sin_family = AF_INET; addr.sin_port = htons(port);
    inet_pton(AF_INET, host.c_str(), &(addr.sin_addr));
    u_long mode = 1; ioctlsocket(sock, FIONBIO, &mode);
    int r = connect(sock, (sockaddr*)&addr, sizeof(addr));
    if (r == SOCKET_ERROR) {
        fd_set wset; FD_ZERO(&wset); FD_SET(sock, &wset);
        timeval tv{ timeoutMs / 1000, (timeoutMs % 1000) * 1000 };
        r = select(0, NULL, &wset, NULL, &tv);
        if (r > 0) { closesocket(sock); return true; }
    }
    closesocket(sock);
    return false;
#else
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return false;
    sockaddr_in addr{}; addr.sin_family = AF_INET; addr.sin_port = htons(port);
    inet_pton(AF_INET, host.c_str(), &(addr.sin_addr));
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);
    int r = connect(sock, (sockaddr*)&addr, sizeof(addr));
    if (r < 0 && errno == EINPROGRESS) {
        fd_set wset; FD_ZERO(&wset); FD_SET(sock, &wset);
        timeval tv{ timeoutMs / 1000, (timeoutMs % 1000) * 1000 };
        r = select(sock + 1, NULL, &wset, NULL, &tv);
        if (r > 0) { close(sock); return true; }
    }
    close(sock);
    return false;
#endif
}

void portScanner(const std::string& host) {
    spinner("Đang quét cổng", 1000, getPalette(CURRENT_THEME).accent);
    std::vector<int> ports = { 21,22,25,53,80,110,143,443,587,3306,3389,8080,8443 };
    std::cout << BLUE << "🔎 Kết quả quét cổng cho " << host << ":" << RESET << "\n";
    for (int p : ports) {
        bool open = tryConnect(host, p);
        std::cout << (open ? GREEN : YELLOW) << "• Port " << p << (open ? " mở" : " đóng") << RESET << "\n";
    }
}

void generatePassword(int length = 12) {
    if (length <= 0 || length > 128) {
        std::cout << YELLOW << "⚠️ Độ dài không hợp lệ (1–128)" << RESET << "\n";
        return;
    }
    const std::string chars =
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()_+";
    std::mt19937 gen(std::random_device{}());
    std::uniform_int_distribution<> dist(0, (int)chars.size() - 1);
    std::string password; password.reserve(length);
    for (int i = 0; i < length; i++) password += chars[dist(gen)];
    std::cout << MAGENTA << "🔑 Mật khẩu ngẫu nhiên: " << password << RESET << "\n";
}

void chooseTheme() {
    showThemeMenu();
    std::cout << "👉 Chọn (1-3): ";
    std::string t; std::getline(std::cin, t);
    if (t == "1") CURRENT_THEME = Theme::Hacker;
    else if (t == "2") CURRENT_THEME = Theme::Cyberpunk;
    else if (t == "3") CURRENT_THEME = Theme::Retro;
    else std::cout << YELLOW << "⚠️ Không hợp lệ, giữ theme hiện tại." << RESET << "\n";
}

void matrixMode() {
    clearScreen();
    typeEffect("🔰 Matrix Mode — nhấn Enter để thoát...", 15);
    matrixRain(20, 40, 80);
    std::string dummy; std::getline(std::cin, dummy);
}

int main() {
#ifdef _WIN32
    system("chcp 65001 > nul");
    WSADATA wsaData;
    (void)WSAStartup(MAKEWORD(2, 2), &wsaData);
#endif

    // Màn chào
    clearScreen();
    asciiLogo();
    typeEffect("🌐 Chào mừng đến với NetHelper CLI — Ultra Deluxe", 35);
    loadingBar(40, 15, getPalette(CURRENT_THEME).accent);
    std::cout << "\n";
    matrixRain(8, 50, 64);
    std::this_thread::sleep_for(std::chrono::milliseconds(300));

    while (true) {
        clearScreen();
        banner();
        auto p = getPalette(CURRENT_THEME);
        std::cout << "\n" << BOLD << "📌 MENU CHỨC NĂNG" << RESET << "\n";
        std::cout << p.primary << "╔════════════════════════════════════════════════════════╗\n";
        std::cout << "║ " << GREEN << " 1." << RESET << p.primary << " Kiểm tra trạng thái web                            ║\n";
        std::cout << "║ " << BLUE << " 2." << RESET << p.primary << " Lấy tiêu đề trang                                  ║\n";
        std::cout << "║ " << YELLOW << " 3." << RESET << p.primary << " Xem HTTP headers                                   ║\n";
        std::cout << "║ " << MAGENTA << " 4." << RESET << p.primary << " Tải HTML về file                                   ║\n";
        std::cout << "║ " << GREEN << " 5." << RESET << p.primary << " Tạo mật khẩu ngẫu nhiên                            ║\n";
        std::cout << "║ " << BLUE << " 6." << RESET << p.primary << " Đo thời gian phản hồi HTTP                         ║\n";
        std::cout << "║ " << YELLOW << " 7." << RESET << p.primary << " Ping website                                       ║\n";
        std::cout << "║ " << MAGENTA << " 8." << RESET << p.primary << " Kiểm tra SSL certificate                           ║\n";
        std::cout << "║ " << GREEN << " 9." << RESET << p.primary << " DNS Lookup                                         ║\n";
        std::cout << "║ " << BLUE << "10." << RESET << p.primary << " Reverse DNS                                        ║\n";
        std::cout << "║ " << YELLOW << "11." << RESET << p.primary << " Traceroute                                         ║\n";
        std::cout << "║ " << MAGENTA << "12." << RESET << p.primary << " Port Scanner                                       ║\n";
        std::cout << "║ " << GREEN << "13." << RESET << p.primary << " Meta Info Extractor                                ║\n";
        std::cout << "║ " << BLUE << "14." << RESET << p.primary << " HTTP Method Tester                                 ║\n";
        std::cout << "║ " << CYAN << "15." << RESET << p.primary << " Đổi theme                                          ║\n";
        std::cout << "║ " << YELLOW << "16." << RESET << p.primary << " Matrix Mode                                        ║\n";
        std::cout << "║ " << RED << " 0." << RESET << p.primary << " Thoát                                              ║\n";
        std::cout << "╚════════════════════════════════════════════════════════╝" << RESET << "\n";
        std::cout << "\n👉 Chọn chức năng (0-16): ";

        std::string choice;
        std::getline(std::cin, choice);

        clearScreen();
        banner();
        std::cout << "\n";

        std::string ua = randomUserAgent();

        if (choice == "1") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            checkStatus(url, ua);

        }
        else if (choice == "2") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            getTitle(url, ua);

        }
        else if (choice == "3") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            showHeaders(url, ua);

        }
        else if (choice == "4") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            std::string filename;
            std::cout << "💾 Tên file lưu (mặc định downloaded.html): ";
            std::getline(std::cin, filename);
            if (filename.empty()) filename = "downloaded.html";
            downloadHTML(url, ua, filename);

        }
        else if (choice == "5") {
            std::string input;
            int length = 12;
            std::cout << "🔢 Nhập độ dài mật khẩu (mặc định 12, Enter để bỏ qua): ";
            std::getline(std::cin, input);
            if (!input.empty()) {
                try { length = std::stoi(input); }
                catch (...) { std::cout << YELLOW << "⚠️ Không phải số, dùng mặc định 12." << RESET << "\n"; length = 12; }
            }
            generatePassword(length);

        }
        else if (choice == "6") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            measureLatency(url, ua);

        }
        else if (choice == "7") {
            std::string host;
            std::cout << "🖧 Nhập domain/host (vd: google.com): ";
            std::getline(std::cin, host);
            pingSite(host);

        }
        else if (choice == "8") {
            std::string url;
            std::cout << "🔗 Nhập URL (https://...): ";
            std::getline(std::cin, url);
            checkSSL(url, ua);

        }
        else if (choice == "9") {
            std::string domain;
            std::cout << "🔎 Nhập domain: ";
            std::getline(std::cin, domain);
            dnsLookup(domain);

        }
        else if (choice == "10") {
            std::string ip;
            std::cout << "🔄 Nhập IP: ";
            std::getline(std::cin, ip);
            reverseDNS(ip);

        }
        else if (choice == "11") {
            std::string host;
            std::cout << "🧭 Nhập domain/host: ";
            std::getline(std::cin, host);
            traceroute(host);

        }
        else if (choice == "12") {
            std::string host;
            std::cout << "🛡️  Nhập IP (vd: 93.184.216.34) hoặc domain đã resolve: ";
            std::getline(std::cin, host);
            addrinfo hints{}, * res;
            hints.ai_family = AF_INET;
            if (getaddrinfo(host.c_str(), nullptr, &hints, &res) == 0 && res) {
                char ipstr[INET_ADDRSTRLEN];
                sockaddr_in* ipv4 = (sockaddr_in*)res->ai_addr;
                inet_ntop(AF_INET, &(ipv4->sin_addr), ipstr, sizeof(ipstr));
                portScanner(ipstr);
                freeaddrinfo(res);
            }
            else {
                portScanner(host);
            }

        }
        else if (choice == "13") {
            std::string url;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            extractMetaInfo(url, ua);

        }
        else if (choice == "14") {
            std::string url, method;
            std::cout << "🔗 Nhập URL: ";
            std::getline(std::cin, url);
            std::cout << "📬 Nhập method (GET/POST/HEAD/OPTIONS): ";
            std::getline(std::cin, method);
            if (method.empty()) method = "GET";
            httpMethodTest(url, method, ua);

        }
        else if (choice == "15") {
            chooseTheme();

        }
        else if (choice == "16") {
            matrixMode();

        }
        else if (choice == "0") {
            std::cout << GREEN << "👋 Tạm biệt NetHelper CLI. Mong bạn sớm quay trở lại nhé!" << RESET << "\n";
#ifdef _WIN32
            WSACleanup();
#endif
            break;

        }
        else {
            std::cout << YELLOW << "⚠️ Lựa chọn không hợp lệ." << RESET << "\n";
        }

        std::cout << "\n" << BOLD << "↩ Nhấn Enter để quay lại menu..." << RESET;
        std::string dummy;
        std::getline(std::cin, dummy);
    }
    return 0;
}
