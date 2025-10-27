import os
import time
import random
import csv
import json
import uuid
from datetime import datetime, timedelta
from colorama import Fore, Style, init

try:
    from plyer import notification
    HAS_NOTIFY = True
except Exception:
    HAS_NOTIFY = False

init(autoreset=True)

DATA_FILE = "taskhelper_users.json"
CSV_FILE = "tasks.csv"

current_user = None
users = {}  # {username: {"password": str, "tasks": [], "archived": [], "habits": [], "xp": int, "level": int, "settings": {...}}}
undo_stack = []  # stack các thao tác cho user hiện tại

greetings = [
    "🔥 Chào mừng bạn quay lại với TaskHelper!",
    "🚀 Hãy cùng chinh phục công việc hôm nay!",
    "🌟 Bạn thật tuyệt, tiếp tục nào!",
    "💡 Một ngày mới, một danh sách mới!"
]

THEMES = {
    "dark": {
        "primary": Fore.CYAN,
        "secondary": Fore.MAGENTA,
        "accent": Fore.YELLOW,
        "dim": Fore.BLUE
    },
    "light": {
        "primary": Fore.BLUE,
        "secondary": Fore.GREEN,
        "accent": Fore.MAGENTA,
        "dim": Fore.CYAN
    }
}

def get_theme():
    if not current_user:
        return THEMES["dark"]
    settings = users[current_user].get("settings", {})
    theme_name = settings.get("theme", "dark")
    return THEMES.get(theme_name, THEMES["dark"])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    th = get_theme()
    print(th["primary"] + Style.BRIGHT + "╔════════════════════════════════════╗")
    print(th["primary"] + Style.BRIGHT + "║          🌐 TaskHelper CLI         ║")
    print(th["primary"] + Style.BRIGHT + "║    🛠️ Công cụ quản lý công việc    ║")
    print(th["primary"] + Style.BRIGHT + "╠════════════════════════════════════╣")
    print(th["dim"]     + Style.DIM    + "║   -----Powered by SliXeR-14-----   ║")
    print(th["dim"]     + Style.DIM    + "║    © 2025 – copyright reversed     ║")
    print(th["primary"] + Style.BRIGHT + "╚════════════════════════════════════╝")
    print(get_theme()["secondary"] + random.choice(greetings))
    if current_user:
        print(get_theme()["accent"] + f"👤 Đang đăng nhập: {current_user}")

def show_menu():
    th = get_theme()
    print(th["accent"] + "\n╔══════════ MENU ═══════════╗")
    print("║ 1. Thêm công việc ➕      ║")
    print("║ 2. Xem danh sách 📋       ║")
    print("║ 3. Đánh dấu hoàn thành ✅ ║")
    print("║ 4. Xóa công việc 🗑️       ║")
    print("║ 5. Tìm kiếm 🔍            ║")
    print("║ 6. Chỉnh sửa ✍️           ║")
    print("║ 7. Sắp xếp 📑             ║")
    print("║ 8. Lưu JSON 💾            ║")
    print("║ 9. Tải JSON 📂            ║")
    print("║ 10. Thống kê 📊           ║")
    print("║ 11. Nhắc deadline ⏰      ║")
    print("║ 12. Xuất CSV 📑           ║")
    print("║ 13. Chọn ngẫu nhiên 🎲    ║")
    print("║ 14. Lọc công việc 🔎      ║")
    print("║ 15. Pomodoro ⏱️           ║")
    print("║ 16. Archive công việc 📦  ║")
    print("║ 17. Xem kho archive 🗃️    ║")
    print("║ 18. Undo ↩️               ║")
    print("║ 19. Kanban Board 🧩       ║")
    print("║ 20. Theo dõi thói quen 🌱 ║")
    print("║ 21. Xuất lịch .ics 📅     ║")
    print("║ 22. Focus Dashboard 🎯    ║")
    print("║ 23. Kế hoạch hằng tuần 🗓️ ║")
    print("║ 24. AI gợi ý 📌           ║")
    print("║ 25. Cài đặt giao diện 🎨  ║")
    print("║ 26. Đăng xuất 🔒          ║")
    print("║ 27. Chuyển tài khoản 👥   ║")
    print("║ 0. Thoát 🚪               ║")
    print("╚═══════════════════════════╝")

def load_all():
    global users
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            print(Fore.RED + f"❌ Lỗi tải dữ liệu người dùng: {e}")
            users = {}
    else:
        users = {}

def save_all():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print("💾 Đã lưu dữ liệu người dùng.")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi lưu dữ liệu: {e}")

def ensure_user(username):
    if username not in users:
        users[username] = {
            "password": "",
            "tasks": [],
            "archived": [],
            "habits": [],
            "xp": 0,
            "level": 1,
            "settings": {"theme": "dark", "pomodoro_work": 25, "pomodoro_rest": 5}
        }

def login():
    global current_user
    print("🔐 Đăng nhập / Đăng ký")
    username = input("👤 Username: ").strip()
    password = input("🔑 Password: ").strip()
    ensure_user(username)
    if not users[username]["password"]:
        users[username]["password"] = password
        print(Fore.GREEN + "✅ Đã tạo tài khoản mới.")
    else:
        if users[username]["password"] != password:
            print(Fore.RED + "❌ Sai mật khẩu.")
            return False
    current_user = username
    return True

def logout():
    global current_user, undo_stack
    current_user = None
    undo_stack = []

def current_tasks():
    return users[current_user]["tasks"]

def current_archived():
    return users[current_user]["archived"]

def current_habits():
    return users[current_user]["habits"]

def new_id():
    return uuid.uuid4().hex[:8]

def read_date(prompt):
    s = input(prompt).strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "❌ Ngày không hợp lệ (YYYY-MM-DD). Bỏ qua.")
        return None

def input_priority():
    p = input("⚡ Ưu tiên (Cao/Trung bình/Thấp): ").strip().lower()
    if p not in ["cao", "trung bình", "thấp"]:
        print(Fore.YELLOW + "ℹ️ Ưu tiên không hợp lệ. Dùng 'trung bình'.")
        p = "trung bình"
    return p

def input_tags():
    s = input("🏷️ Tag (phân cách bằng dấu phẩy, Enter nếu bỏ qua): ").strip()
    if not s:
        return []
    return [t.strip().lower() for t in s.split(",") if t.strip()]

def input_repeat():
    s = input("🔁 Lặp lại (none/daily/weekly/monthly): ").strip().lower()
    if s not in ["none", "daily", "weekly", "monthly", ""]:
        print(Fore.YELLOW + "ℹ️ Giá trị lặp lại không hợp lệ. Dùng 'none'.")
        s = "none"
    return s if s else "none"

def input_status():
    s = input("📦 Trạng thái (todo/doing/done): ").strip().lower()
    if s not in ["todo", "doing", "done"]:
        print(Fore.YELLOW + "ℹ️ Trạng thái không hợp lệ. Dùng 'todo'.")
        s = "todo"
    return s

def color_for_priority(p):
    return Fore.RED if p == "cao" else (Fore.YELLOW if p == "trung bình" else Fore.CYAN)

def confirm(prompt):
    ans = input(f"{prompt} (y/n): ").strip().lower()
    return ans == "y"

def find_task_by_id(tid):
    for idx, t in enumerate(current_tasks()):
        if t["id"] == tid:
            return idx, t
    return None, None

def gain_xp(points=10):
    user = users[current_user]
    user["xp"] = user.get("xp", 0) + points
    while user["xp"] >= user["level"] * 100:
        user["xp"] -= user["level"] * 100
        user["level"] += 1
        print(Fore.MAGENTA + f"🏆 Chúc mừng! Bạn đã lên cấp {user['level']}!")

def show_profile():
    u = users[current_user]
    print(f"👤 {current_user} | Level: {u.get('level',1)} | XP: {u.get('xp',0)}")

def add_task():
    name = input("✍️ Nhập công việc mới: ").strip()
    if not name:
        print(Fore.RED + "❌ Tên công việc không được rỗng.")
        return
    deadline_dt = read_date("📅 Hạn chót (YYYY-MM-DD, Enter nếu bỏ qua): ")
    priority = input_priority()
    tags = input_tags()
    repeat = input_repeat()
    status = input_status()

    task = {
        "id": new_id(),
        "name": name,
        "done": status == "done",
        "status": status,  # Kanban: todo/doing/done
        "created": datetime.now().isoformat(),
        "deadline": deadline_dt.strftime("%Y-%m-%d") if deadline_dt else None,
        "priority": priority,
        "tags": tags,
        "repeat": repeat
    }
    current_tasks().append(task)
    undo_stack.append(("add", task["id"]))
    print(Fore.GREEN + "✅ Đã thêm công việc!")

def view_tasks():
    tasks = current_tasks()
    if not tasks:
        print("📭 Chưa có công việc nào.")
        return
    show_profile()
    print("\n📋 Danh sách công việc:")
    for i, t in enumerate(tasks, 1):
        status_icon = Fore.GREEN + "✅" if t["done"] else Fore.RED + "❌"
        color = color_for_priority(t["priority"])
        deadline = t["deadline"] or "Không"
        created = datetime.fromisoformat(t["created"]).strftime("%Y-%m-%d %H:%M")
        tag_str = ", ".join(t["tags"]) if t["tags"] else "—"
        repeat = t["repeat"]
        print(f"{i}. [{t['id']}] {t['name']} {status_icon} | Trạng thái: {t['status']} | Ưu tiên: {color}{t['priority']}{Style.RESET_ALL} | Deadline: {deadline} | Tạo: {created} | Tag: {tag_str} | Lặp: {repeat}")
    show_progress()

def mark_done():
    if not current_tasks():
        print("📭 Không có công việc.")
        return
    view_tasks()
    tid = input("🔢 Nhập ID công việc hoàn thành: ").strip()
    idx, t = find_task_by_id(tid)
    if t:
        if t["done"]:
            print("ℹ️ Công việc đã hoàn thành trước đó.")
            return
        t["done"] = True
        t["status"] = "done"
        undo_stack.append(("done", tid))
        print(Fore.GREEN + "🎉 Đã đánh dấu hoàn thành!")
        gain_xp(20)  # thưởng XP khi hoàn thành
        handle_repeat(t)
    else:
        print(Fore.RED + "❌ Không tìm thấy ID.")

def handle_repeat(task):
    repeat = task.get("repeat", "none")
    if repeat == "none":
        return
    if not task.get("deadline"):
        return
    try:
        current = datetime.strptime(task["deadline"], "%Y-%m-%d")
    except ValueError:
        return

    if repeat == "daily":
        next_deadline = current + timedelta(days=1)
    elif repeat == "weekly":
        next_deadline = current + timedelta(weeks=1)
    elif repeat == "monthly":
        next_deadline = current + timedelta(days=30)
    else:
        return

    new_task = {
        "id": new_id(),
        "name": task["name"],
        "done": False,
        "status": "todo",
        "created": datetime.now().isoformat(),
        "deadline": next_deadline.strftime("%Y-%m-%d"),
        "priority": task["priority"],
        "tags": task["tags"][:],
        "repeat": task["repeat"]
    }
    current_tasks().append(new_task)
    print(Fore.CYAN + f"🔁 Đã tạo công việc lặp tiếp theo với deadline {new_task['deadline']}")

def delete_task():
    if not current_tasks():
        print("📭 Không có công việc.")
        return
    view_tasks()
    tid = input("🔢 Nhập ID công việc cần xóa: ").strip()
    idx, t = find_task_by_id(tid)
    if t:
        if not confirm(f"🗑️ Xác nhận xóa '{t['name']}'?"):
            print("❎ Đã hủy.")
            return
        removed = current_tasks().pop(idx)
        undo_stack.append(("delete", removed))  # lưu toàn bộ để undo
        print(Fore.GREEN + f"🗑️ Đã xóa: {removed['name']}")
    else:
        print(Fore.RED + "❌ Không tìm thấy ID.")

def search_task():
    keyword = input("🔍 Từ khóa: ").strip().lower()
    found = [t for t in current_tasks() if keyword in t["name"].lower()]
    if not found:
        print("😕 Không tìm thấy công việc nào.")
    else:
        print("\n🔎 Kết quả tìm kiếm:")
        for i, t in enumerate(found, 1):
            status = "✅" if t["done"] else "❌"
            print(f"{i}. [{t['id']}] {t['name']} {status} | Trạng thái: {t['status']}")

def edit_task():
    if not current_tasks():
        print("📭 Không có công việc.")
        return
    view_tasks()
    tid = input("✍️ Nhập ID công việc cần sửa: ").strip()
    idx, t = find_task_by_id(tid)
    if not t:
        print(Fore.RED + "❌ Không tìm thấy ID.")
        return

    before = json.dumps(t, ensure_ascii=False)
    print("🧩 Trường có thể sửa: name, deadline, priority, tags, repeat, status")
    field = input("🔤 Trường: ").strip().lower()
    if field not in ["name", "deadline", "priority", "tags", "repeat", "status"]:
        print(Fore.RED + "❌ Trường không hợp lệ.")
        return

    if field == "name":
        new_name = input("🔤 Tên mới: ").strip()
        if not new_name:
            print(Fore.RED + "❌ Tên không được rỗng.")
            return
        t["name"] = new_name
    elif field == "deadline":
        new_deadline = read_date("📅 Deadline mới (YYYY-MM-DD hoặc Enter để xóa): ")
        t["deadline"] = new_deadline.strftime("%Y-%m-%d") if new_deadline else None
    elif field == "priority":
        t["priority"] = input_priority()
    elif field == "tags":
        t["tags"] = input_tags()
    elif field == "repeat":
        t["repeat"] = input_repeat()
    elif field == "status":
        s = input_status()
        t["status"] = s
        t["done"] = (s == "done")

    undo_stack.append(("edit", tid, before))
    print(Fore.GREEN + "✏️ Đã cập nhật công việc!")

def sort_tasks():
    tasks = current_tasks()
    if not tasks:
        print("📭 Không có công việc để sắp xếp.")
        return
    print("1. Theo tên (A-Z)")
    print("2. Theo trạng thái (chưa xong trước)")
    print("3. Theo ưu tiên (Cao → Thấp)")
    print("4. Theo deadline (gần nhất → xa)")
    print("5. Theo trạng thái Kanban (todo→doing→done)")
    choice = input("👉 Chọn: ").strip()
    if choice == "1":
        tasks.sort(key=lambda x: x["name"].lower())
    elif choice == "2":
        tasks.sort(key=lambda x: x["done"])
    elif choice == "3":
        order = {"cao": 0, "trung bình": 1, "thấp": 2}
        tasks.sort(key=lambda x: order.get(x["priority"], 3))
    elif choice == "4":
        def key_deadline(x):
            if not x["deadline"]:
                return datetime.max
            try:
                return datetime.strptime(x["deadline"], "%Y-%m-%d")
            except ValueError:
                return datetime.max
        tasks.sort(key=key_deadline)
    elif choice == "5":
        order = {"todo": 0, "doing": 1, "done": 2}
        tasks.sort(key=lambda x: order.get(x["status"], 3))
    print("📑 Đã sắp xếp!")

def save_tasks():
    save_all()

def load_tasks():
    load_all()
    print("📂 Đã tải dữ liệu.")

def stats():
    tasks = current_tasks()
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    undone = total - done
    by_priority = {"cao": 0, "trung bình": 0, "thấp": 0}
    for t in tasks:
        by_priority[t["priority"]] = by_priority.get(t["priority"], 0) + 1
    print(f"\n📊 Thống kê:")
    print(f"   Tổng số công việc: {total}")
    print(f"   Đã hoàn thành: {Fore.GREEN}{done}{Style.RESET_ALL}")
    print(f"   Chưa hoàn thành: {Fore.RED}{undone}{Style.RESET_ALL}")
    print(f"   Ưu tiên: Cao={by_priority['cao']}, Trung bình={by_priority['trung bình']}, Thấp={by_priority['thấp']}")
    show_progress()

def show_progress():
    tasks = current_tasks()
    total = len(tasks)
    if total == 0:
        return
    done = sum(1 for t in tasks if t["done"])
    percent = int((done / total) * 100)
    bar = "█" * (percent // 10) + "-" * (10 - percent // 10)
    print(f"\n⏳ Tiến độ: [{bar}] {percent}%")

def notify(title, message):
    if HAS_NOTIFY:
        try:
            notification.notify(title=title, message=message, timeout=5)
        except Exception:
            pass

def remind_deadlines():
    print("\n⏰ Công việc sắp đến hạn (≤ 2 ngày):")
    now = datetime.now()
    upcoming = []
    for t in current_tasks():
        if t["deadline"] and not t["done"]:
            try:
                d = datetime.strptime(t["deadline"], "%Y-%m-%d")
                if d - now <= timedelta(days=2):
                    upcoming.append(t)
            except ValueError:
                pass
    if not upcoming:
        print("👍 Không có công việc nào sắp hết hạn.")
    else:
        for t in upcoming:
            msg = f"[{t['id']}] {t['name']} - Deadline: {t['deadline']} - Ưu tiên: {t['priority']}"
            print(f"⚠️ {msg}")
            notify("Nhắc nhở deadline", msg)

def export_csv():
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["User", "ID", "Tên", "Trạng thái", "Ưu tiên", "Deadline", "Ngày tạo", "Tag", "Lặp"])
            for uname, data in users.items():
                for t in data["tasks"]:
                    writer.writerow([
                        uname,
                        t["id"],
                        t["name"],
                        t["status"],
                        t["priority"],
                        t["deadline"] or "",
                        t["created"],
                        ",".join(t["tags"]),
                        t["repeat"]
                    ])
        print(f"💾 Đã xuất CSV: {CSV_FILE}")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi xuất CSV: {e}")

def random_task():
    undone = [t for t in current_tasks() if not t["done"]]
    if not undone:
        print("🎉 Tất cả công việc đã hoàn thành!")
    else:
        def score(t):
            dl = datetime.strptime(t["deadline"], "%Y-%m-%d") if t["deadline"] else datetime.max
            pri = {"cao": 0, "trung bình": 1, "thấp": 2}[t["priority"]]
            return (pri, dl)
        undone.sort(key=score)
        chosen = random.choice(undone[:max(1, len(undone)//3)])
        print(f"🎲 Hãy làm: {Fore.CYAN}[{chosen['id']}] {chosen['name']}{Style.RESET_ALL} (Ưu tiên: {chosen['priority']}, Deadline: {chosen['deadline'] or 'Không'})")

def filter_tasks():
    print("📌 Lọc theo: done / undone / cao / trung bình / thấp / tag:<tên> / status:<todo|doing|done>")
    choice = input("👉 Nhập lựa chọn: ").strip().lower()
    tasks = current_tasks()
    filtered = []
    if choice == "done":
        filtered = [t for t in tasks if t["done"]]
    elif choice == "undone":
        filtered = [t for t in tasks if not t["done"]]
    elif choice in ["cao", "trung bình", "thấp"]:
        filtered = [t for t in tasks if t["priority"] == choice]
    elif choice.startswith("tag:"):
        tag = choice.split(":", 1)[1].strip()
        filtered = [t for t in tasks if tag in t["tags"]]
    elif choice.startswith("status:"):
        st = choice.split(":", 1)[1].strip()
        filtered = [t for t in tasks if t["status"] == st]
    else:
        print("❌ Lựa chọn không hợp lệ.")
        return
    if not filtered:
        print("📭 Không có công việc phù hợp.")
    else:
        for i, t in enumerate(filtered, 1):
            status = "✅" if t["done"] else "❌"
            print(f"{i}. [{t['id']}] {t['name']} | Ưu tiên: {t['priority']} | Trạng thái: {t['status']} | {status}")

def pomodoro():
    settings = users[current_user].get("settings", {})
    default_work = settings.get("pomodoro_work", 25)
    default_rest = settings.get("pomodoro_rest", 5)
    print(f"⏱️ Pomodoro: {default_work} phút làm việc, {default_rest} phút nghỉ")
    try:
        work = int(input(f"⏳ Thời gian làm (phút, mặc định {default_work}): ") or str(default_work))
        rest = int(input(f"😌 Thời gian nghỉ (phút, mặc định {default_rest}): ") or str(default_rest))
    except ValueError:
        print(Fore.RED + "❌ Giá trị không hợp lệ. Dùng mặc định.")
        work, rest = default_work, default_rest

    focus_id = input("🎯 ID công việc để focus (Enter nếu bỏ qua): ").strip()
    focus_task = None
    if focus_id:
        _, focus_task = find_task_by_id(focus_id)
        if focus_task:
            print(Fore.CYAN + f"🎯 Focus: {focus_task['name']}")
        else:
            print(Fore.YELLOW + "ℹ️ Không tìm thấy ID, tiếp tục không focus.")

    def countdown(minutes, label):
        total = minutes * 60
        for sec in range(total, -1, -1):
            percent = int(((total - sec) / total) * 100) if total else 100
            bar = "█" * (percent // 10) + "-" * (10 - percent // 10)
            print(f"\r{label}: [{bar}] {percent}% | Còn {sec//60:02d}:{sec%60:02d}", end="")
            time.sleep(1)
        print()

    print(Fore.GREEN + "🏁 Bắt đầu phiên làm việc!")
    countdown(work, "Làm việc")
    print(Fore.CYAN + "☕ Nghỉ thôi!")
    countdown(rest, "Nghỉ")
    print(Fore.MAGENTA + "✅ Hoàn tất một chu kỳ Pomodoro!")

    if focus_task and confirm("Đánh dấu công việc đã hoàn thành?"):
        focus_task["done"] = True
        focus_task["status"] = "done"
        undo_stack.append(("done", focus_task["id"]))
        gain_xp(20)
        print(Fore.GREEN + "🎉 Đã đánh dấu hoàn thành!")

def archive_task():
    if not current_tasks():
        print("📭 Không có công việc.")
        return
    view_tasks()
    tid = input("📦 Nhập ID cần archive: ").strip()
    idx, t = find_task_by_id(tid)
    if not t:
        print(Fore.RED + "❌ Không tìm thấy ID.")
        return
    current_archived().append(t)
    current_tasks().pop(idx)
    undo_stack.append(("archive", t))
    print(Fore.GREEN + f"📦 Đã chuyển '{t['name']}' vào archive.")

def view_archive():
    arch = current_archived()
    if not arch:
        print("🗃️ Archive trống.")
        return
    print("\n🗃️ Danh sách archive:")
    for i, t in enumerate(arch, 1):
        status = "✅" if t["done"] else "❌"
        print(f"{i}. [{t['id']}] {t['name']} ({status}) | Tag: {', '.join(t['tags']) if t['tags'] else '—'}")

def undo():
    if not undo_stack:
        print("ℹ️ Không có thao tác để undo.")
        return
    action = undo_stack.pop()
    kind = action[0]
    if kind == "add":
        tid = action[1]
        idx, t = find_task_by_id(tid)
        if t:
            current_tasks().pop(idx)
            print("↩️ Đã undo: thêm công việc.")
    elif kind == "delete":
        removed = action[1]
        current_tasks().append(removed)
        print("↩️ Đã undo: xóa công việc.")
    elif kind == "edit":
        tid, before_json = action[1], action[2]
        idx, t = find_task_by_id(tid)
        if t:
            before = json.loads(before_json)
            current_tasks()[idx] = before
            print("↩️ Đã undo: sửa công việc.")
    elif kind == "done":
        tid = action[1]
        idx, t = find_task_by_id(tid)
        if t:
            t["done"] = False
            t["status"] = "todo"
            print("↩️ Đã undo: đánh dấu hoàn thành.")
    elif kind == "archive":
        archived_item = action[1]
        for i, a in enumerate(current_archived()):
            if a["id"] == archived_item["id"]:
                current_tasks().append(a)
                current_archived().pop(i)
                print("↩️ Đã undo: archive.")
                break
    else:
        print("⚠️ Không hỗ trợ undo cho thao tác này.")

def kanban_board():
    tasks = current_tasks()
    cols = {"todo": [], "doing": [], "done": []}
    for t in tasks:
        cols.setdefault(t["status"], []).append(t)

    print("\n🧩 Kanban Board")
    def print_col(name, items):
        print(get_theme()["primary"] + f"\n— {name.upper()} —")
        for t in items:
            pri = color_for_priority(t["priority"])
            print(f"[{t['id']}] {t['name']} | Ưu tiên: {pri}{t['priority']}{Style.RESET_ALL} | Deadline: {t['deadline'] or 'Không'}")

    print_col("todo", cols.get("todo", []))
    print_col("doing", cols.get("doing", []))
    print_col("done", cols.get("done", []))

    if confirm("Chuyển trạng thái công việc?"):
        tid = input("ID công việc: ").strip()
        _, t = find_task_by_id(tid)
        if not t:
            print(Fore.RED + "❌ Không tìm thấy ID.")
            return
        print("Trạng thái mới: todo / doing / done")
        new_status = input_status()
        before = json.dumps(t, ensure_ascii=False)
        t["status"] = new_status
        t["done"] = (new_status == "done")
        undo_stack.append(("edit", t["id"], before))
        print(Fore.GREEN + "🔄 Đã cập nhật trạng thái.")

def add_habit():
    name = input("🌱 Nhập thói quen mới: ").strip()
    if not name:
        print(Fore.RED + "❌ Tên thói quen không được rỗng.")
        return
    current_habits().append({"name": name, "streak": 0, "last_done": None})
    print(Fore.GREEN + "✅ Đã thêm thói quen!")

def mark_habit_done():
    habits = current_habits()
    if not habits:
        print("📭 Chưa có thói quen nào.")
        return
    print("\n🌱 Danh sách thói quen:")
    for i, h in enumerate(habits, 1):
        print(f"{i}. {h['name']} (Streak: {h['streak']}) - Last: {h['last_done'] or '—'}")
    try:
        idx = int(input("🔢 Chọn thói quen đã làm hôm nay: ")) - 1
        if 0 <= idx < len(habits):
            today = datetime.now().date()
            last = habits[idx]["last_done"]
            if last == str(today):
                print("ℹ️ Hôm nay bạn đã đánh dấu rồi.")
            else:
                if last == str(today - timedelta(days=1)):
                    habits[idx]["streak"] += 1
                else:
                    habits[idx]["streak"] = 1
                habits[idx]["last_done"] = str(today)
                print(Fore.MAGENTA + f"🎉 Giữ streak {habits[idx]['streak']} ngày!")
                gain_xp(5)  # thưởng XP nhỏ cho thói quen
        else:
            print(Fore.RED + "❌ Không hợp lệ.")
    except ValueError:
        print(Fore.RED + "❌ Vui lòng nhập số.")

def view_habits():
    habits = current_habits()
    if not habits:
        print("📭 Chưa có thói quen nào.")
        return
    print("\n🌱 Thói quen:")
    for i, h in enumerate(habits, 1):
        print(f"{i}. {h['name']} | Streak: {h['streak']} | Last: {h['last_done'] or '—'}")

def habit_menu():
    print("\n🌱 Habit Tracker")
    print("1. Thêm thói quen")
    print("2. Đánh dấu đã làm hôm nay")
    print("3. Xem thói quen")
    choice = input("👉 Chọn (1-3): ").strip()
    if choice == "1":
        add_habit()
    elif choice == "2":
        mark_habit_done()
    elif choice == "3":
        view_habits()
    else:
        print("❌ Lựa chọn không hợp lệ.")

def export_ics():
    tasks = current_tasks()
    events = []
    for t in tasks:
        if t["deadline"]:
            dt = datetime.strptime(t["deadline"], "%Y-%m-%d")
            dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
            uid = t["id"]
            summary = t["name"].replace("\n", " ")
            start = dt.strftime("%Y%m%d")
            end = (dt + timedelta(days=1)).strftime("%Y%m%d")
            event = [
                "BEGIN:VEVENT",
                f"DTSTAMP:{dtstamp}",
                f"UID:{uid}",
                f"SUMMARY:{summary}",
                f"DTSTART;VALUE=DATE:{start}",
                f"DTEND;VALUE=DATE:{end}",
                "END:VEVENT"
            ]
            events.extend(event)

    if not events:
        print("📭 Không có công việc có deadline để xuất .ics")
        return

    content = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//TaskHelper//VN//EN"]
    content.extend(events)
    content.append("END:VCALENDAR")

    ics_file = "tasks.ics"
    try:
        with open(ics_file, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        print(Fore.GREEN + f"📅 Đã xuất lịch: {ics_file} (import vào Google Calendar/Outlook)")
    except Exception as e:
        print(Fore.RED + f"❌ Lỗi xuất .ics: {e}")

def focus_dashboard():
    tasks = current_tasks()
    today = datetime.now().date()
    candidate = [t for t in tasks if not t["done"]]
    def score(t):
        dl = datetime.strptime(t["deadline"], "%Y-%m-%d").date() if t["deadline"] else datetime.max.date()
        pri = {"cao": 0, "trung bình": 1, "thấp": 2}[t["priority"]]
        return (pri, dl)
    candidate.sort(key=score)
    top = candidate[0] if candidate else None

    habits = current_habits()
    need_habits = [h for h in habits if h.get("last_done") != str(today)]

    show_profile()
    print("\n🎯 Focus Dashboard")
    if top:
        print(Fore.CYAN + f"- Việc ưu tiên: [{top['id']}] {top['name']} (Ưu tiên: {top['priority']}, Deadline: {top['deadline'] or 'Không'})")
    else:
        print(Fore.CYAN + "- Không có việc ưu tiên (danh sách trống hoặc đã xong).")
    if need_habits:
        print(Fore.GREEN + f"- Thói quen cần làm hôm nay ({len(need_habits)}): " + ", ".join(h["name"] for h in need_habits))
    else:
        print(Fore.GREEN + "- Tất cả thói quen đã được đánh dấu hôm nay.")
    show_progress()

def weekly_planner():
    tasks = current_tasks()
    today = datetime.now().date()
    start_week = today - timedelta(days=today.weekday())  # Monday
    days = [start_week + timedelta(days=i) for i in range(7)]
    plan = {d.strftime("%Y-%m-%d"): [] for d in days}

    for t in tasks:
        if t["deadline"]:
            try:
                d = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
                if d in days:
                    plan[d.strftime("%Y-%m-%d")].append(t)
            except ValueError:
                pass

    print("\n🗓️ Weekly Planner (Mon-Sun):")
    for d in days:
        key = d.strftime("%Y-%m-%d")
        label = d.strftime("%a %d/%m")
        items = plan[key]
        print(get_theme()["primary"] + f"\n{label}")
        if not items:
            print("  — Không có công việc —")
        else:
            for t in sorted(items, key=lambda x: {"cao":0,"trung bình":1,"thấp":2}[x["priority"]]):
                mark = "✅" if t["done"] else "•"
                print(f"  {mark} [{t['id']}] {t['name']} (Ưu tiên: {t['priority']})")

def ai_suggest():
    tasks = current_tasks()
    undone = [t for t in tasks if not t["done"]]
    if not undone:
        print("🎉 Không có việc cần gợi ý (tất cả đã xong).")
        return

    # Gợi ý deadline nếu thiếu: dựa vào ưu tiên
    missing_deadline = [t for t in undone if not t["deadline"]]
    for t in missing_deadline:
        if t["priority"] == "cao":
            suggest = datetime.now().date() + timedelta(days=2)
        elif t["priority"] == "trung bình":
            suggest = datetime.now().date() + timedelta(days=5)
        else:
            suggest = datetime.now().date() + timedelta(days=10)
        print(Fore.YELLOW + f"📌 Gợi ý deadline cho [{t['id']}] {t['name']}: {suggest.strftime('%Y-%m-%d')}")

    # Gợi ý thứ tự làm: top 5 việc theo (ưu tiên, deadline)
    def rank(t):
        dl = datetime.strptime(t["deadline"], "%Y-%m-%d") if t["deadline"] else datetime.max
        pri = {"cao": 0, "trung bình": 1, "thấp": 2}[t["priority"]]
        return (pri, dl)
    order = sorted(undone, key=rank)[:5]
    print("\n📋 Nên làm trước (top 5):")
    for i, t in enumerate(order, 1):
        print(f" {i}. [{t['id']}] {t['name']} (Ưu tiên: {t['priority']}, Deadline: {t['deadline'] or 'Không'})")

def settings_menu():
    print("\n🎨 Cài đặt")
    print("1. Chọn theme (dark/light)")
    print("2. Thiết lập Pomodoro (work/rest)")
    choice = input("👉 Chọn (1-2): ").strip()
    if choice == "1":
        theme = input("Theme (dark/light): ").strip().lower()
        if theme not in THEMES:
            print(Fore.RED + "❌ Theme không hợp lệ.")
            return
        users[current_user]["settings"]["theme"] = theme
        print(Fore.GREEN + "🎨 Đã cập nhật theme.")
    elif choice == "2":
        try:
            work = int(input("Thời gian làm (phút): ").strip())
            rest = int(input("Thời gian nghỉ (phút): ").strip())
            users[current_user]["settings"]["pomodoro_work"] = max(1, work)
            users[current_user]["settings"]["pomodoro_rest"] = max(1, rest)
            print(Fore.GREEN + "⏱️ Đã cập nhật Pomodoro.")
        except ValueError:
            print(Fore.RED + "❌ Giá trị không hợp lệ.")
    else:
        print("❌ Lựa chọn không hợp lệ.")

def main():
    load_all()
    while not current_user:
        if not login():
            if not confirm("Thử lại đăng nhập?"):
                print("👋 Tạm biệt!")
                return

    while True:
        clear_screen()
        banner()
        show_menu()
        choice = input("\n👉 Chọn chức năng (0-99): ").strip()

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
        elif choice == "11":
            remind_deadlines()
        elif choice == "12":
            export_csv()
        elif choice == "13":
            random_task()
        elif choice == "14":
            filter_tasks()
        elif choice == "15":
            pomodoro()
        elif choice == "16":
            archive_task()
        elif choice == "17":
            view_archive()
        elif choice == "18":
            undo()
        elif choice == "19":
            kanban_board()
        elif choice == "20":
            habit_menu()
        elif choice == "21":
            export_ics()
        elif choice == "22":
            focus_dashboard()
        elif choice == "23":
            weekly_planner()
        elif choice == "24":
            ai_suggest()
        elif choice == "25":
            settings_menu()
        elif choice == "26":
            logout()
            print("🔒 Đã đăng xuất.")
            if not confirm("Đăng nhập tài khoản khác ngay?"):
                break
            if not login():
                print("👋 Tạm biệt!")
                break
        elif choice == "27":
            if login():
                print(Fore.GREEN + "🔄 Đã chuyển tài khoản.")
        elif choice == "0":
            print("👋 Tạm biệt, hẹn gặp lại!")
            time.sleep(1)
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")

        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
