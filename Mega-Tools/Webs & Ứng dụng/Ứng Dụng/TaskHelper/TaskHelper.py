import os
import time
import random
from colorama import Fore, Style, init

init(autoreset=True)

tasks = []

greetings = [
    "🔥 Chào mừng bạn quay lại với TaskHelper!",
    "🚀 Hãy cùng chinh phục công việc hôm nay!",
    "🌟 Bạn thật tuyệt, tiếp tục nào!",
    "💡 Một ngày mới, một danh sách mới!"
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + Style.BRIGHT + "╔════════════════════════════════════╗")
    print(Fore.CYAN + Style.BRIGHT + "║          🌐 TaskHelper CLI         ║")
    print(Fore.CYAN + Style.BRIGHT + "║    🛠️ Công cụ quản lý công việc    ║")
    print(Fore.CYAN + Style.BRIGHT + "╠════════════════════════════════════╣")
    print(Fore.BLUE + Style.DIM    + "║   -----Powered by SliXeR-14-----   ║")
    print(Fore.BLUE + Style.DIM    + "║    © 2025 – copyright reversed     ║")
    print(Fore.CYAN + Style.BRIGHT + "╚════════════════════════════════════╝")
    print(Fore.MAGENTA + random.choice(greetings))

def show_menu():
    print(Fore.YELLOW + "\n╔══════════ MENU ═══════════╗")
    print("║ 1. Thêm công việc ➕      ║")
    print("║ 2. Xem danh sách 📋       ║")
    print("║ 3. Đánh dấu hoàn thành ✅ ║")
    print("║ 4. Xóa công việc 🗑️       ║")
    print("║ 5. Tìm kiếm 🔍            ║")
    print("║ 6. Chỉnh sửa ✍️           ║")
    print("║ 7. Sắp xếp 📑             ║")
    print("║ 8. Lưu công việc 💾       ║")
    print("║ 9. Tải công việc 📂       ║")
    print("║ 10. Thống kê 📊           ║")
    print("║ 0. Thoát 🚪               ║")
    print("╚═══════════════════════════╝")

def add_task():
    task = input("✍️ Nhập công việc mới: ")
    tasks.append({"name": task, "done": False})
    print("✅ Đã thêm!")

def view_tasks():
    if not tasks:
        print("📭 Chưa có công việc nào.")
    else:
        print("\n📋 Danh sách công việc:")
        for i, t in enumerate(tasks, 1):
            status = Fore.GREEN + "✅" if t["done"] else Fore.RED + "❌"
            print(f"{i}. {t['name']} {status}")
        show_progress()

def mark_done():
    view_tasks()
    if tasks:
        try:
            index = int(input("🔢 Nhập số thứ tự công việc hoàn thành: "))
            if 1 <= index <= len(tasks):
                tasks[index-1]["done"] = True
                print("🎉 Đã đánh dấu hoàn thành!")
            else:
                print("❌ Không hợp lệ.")
        except ValueError:
            print("❌ Vui lòng nhập số.")

def delete_task():
    view_tasks()
    if tasks:
        try:
            index = int(input("🔢 Nhập số thứ tự công việc cần xóa: "))
            if 1 <= index <= len(tasks):
                removed = tasks.pop(index-1)
                print(f"🗑️ Đã xóa: {removed['name']}")
            else:
                print("❌ Không hợp lệ.")
        except ValueError:
            print("❌ Vui lòng nhập số.")

def search_task():
    keyword = input("🔍 Nhập từ khóa tìm kiếm: ").lower()
    found = [t for t in tasks if keyword in t["name"].lower()]
    if not found:
        print("😕 Không tìm thấy công việc nào.")
    else:
        print("\n🔎 Kết quả tìm kiếm:")
        for i, t in enumerate(found, 1):
            status = "✅" if t["done"] else "❌"
            print(f"{i}. {t['name']} {status}")

def edit_task():
    view_tasks()
    if tasks:
        try:
            index = int(input("✍️ Nhập số thứ tự công việc cần sửa: "))
            if 1 <= index <= len(tasks):
                new_name = input("🔤 Nhập tên mới: ")
                tasks[index-1]["name"] = new_name
                print("✏️ Đã cập nhật công việc!")
            else:
                print("❌ Không hợp lệ.")
        except ValueError:
            print("❌ Vui lòng nhập số.")

def sort_tasks():
    if not tasks:
        print("📭 Không có công việc để sắp xếp.")
        return
    print("1. Sắp xếp theo tên (A-Z)")
    print("2. Sắp xếp theo trạng thái (chưa xong trước)")
    choice = input("👉 Chọn cách sắp xếp: ")
    if choice == "1":
        tasks.sort(key=lambda x: x["name"].lower())
    elif choice == "2":
        tasks.sort(key=lambda x: x["done"])
    print("📑 Đã sắp xếp!")

def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(f"{t['name']}|{t['done']}\n")
    print("💾 Đã lưu công việc vào tasks.txt")

def load_tasks():
    global tasks
    if not os.path.exists("tasks.txt"):
        print("📂 Chưa có file lưu.")
        return
    with open("tasks.txt", "r", encoding="utf-8") as f:
        tasks = []
        for line in f:
            name, done = line.strip().split("|")
            tasks.append({"name": name, "done": done == "True"})
    print("📂 Đã tải công việc từ file.")

def stats():
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    undone = total - done
    print(f"\n📊 Thống kê:")
    print(f"   Tổng số công việc: {total}")
    print(f"   Đã hoàn thành: {Fore.GREEN}{done}")
    print(f"   Chưa hoàn thành: {Fore.RED}{undone}")
    show_progress()

def show_progress():
    total = len(tasks)
    if total == 0:
        return
    done = sum(1 for t in tasks if t["done"])
    percent = int((done / total) * 100)
    bar = "█" * (percent // 10) + "-" * (10 - percent // 10)
    print(f"\n⏳ Tiến độ: [{bar}] {percent}%")

def main():
    while True:
        clear_screen()
        banner()
        show_menu()
        choice = input("\n👉 Chọn chức năng (0-10): ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            search_task()
        elif choice == "6":
            edit_task()
        elif choice == "7":
            sort_tasks()
        elif choice == "8":
            save_tasks()
        elif choice == "9":
            load_tasks()
        elif choice == "10":
            stats()
        elif choice == "0":
            print("👋 Tạm biệt, hẹn gặp lại!")
            time.sleep(1)
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")
        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
