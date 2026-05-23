import psutil
import csv
import os
import time
import datetime
import smtplib
import threading
from email.mime.text import MIMEText

#default alert thresholds (user can change from menu)
cpu_limit = 80
ram_limit = 80
disk_limit = 90

# log file path
log_file = "system_log.csv"

#  flag to control monitoring loop
keep_running = False

#create log file with header if it doesnot exist
def setup_log():
    if not os.path.exists(log_file):
        with open(log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "CPU(%)", "RAM(%)", "Disk(%)"])

# get current cpu ram and disk usage
def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return cpu, ram, disk

#save one reading to csv log
def save_to_log(cpu, ram, disk):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, cpu, ram, disk])

#check if any stat crossed its threshold and print alert
def check_alerts(cpu, ram, disk):
    if cpu > cpu_limit:
        print(f"  [ALERT] CPU usage is HIGH: {cpu}%  (limit: {cpu_limit}%)")
    if ram > ram_limit:
        print(f"  [ALERT] RAM usage is HIGH: {ram}%  (limit: {ram_limit}%)")
    if disk > disk_limit:
        print(f"  [ALERT] DISK usage is HIGH: {disk}%  (limit: {disk_limit}%)")

# draw a simple ascii bar so output looks clean
def draw_bar(label, value, limit):
    filled = int(value / 5)
    bar = "#" * filled + "-" * (20 - filled)
    status = "OK" if value < limit else "!!"
    print(f"  {label:<6} [{bar}] {value:5.1f}%  [{status}]")

# bonus: send email alert (user fills credentials)
def send_email_alert(subject, body, to_email, from_email, app_password):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("  [EMAIL] Alert email sent successfully.")
    except Exception as error:
        print(f"  [EMAIL ERROR] {error}")

# bonus: desktop notification via plyer (optional install)
def send_desktop_notification(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=5)
    except ImportError:
        pass

#core monitoring loop that runs in background thread
def monitor_loop(interval, use_email, email_info):
    global keep_running
    setup_log()
    print("\n  Monitoring started. Press Ctrl+C or choose Exit to stop.\n")
    while keep_running:
        cpu, ram, disk = get_stats()
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 46)
        print("   SYSTEM RESOURCE MONITOR  |  Live View")
        print("=" * 46)
        draw_bar("CPU", cpu, cpu_limit)
        draw_bar("RAM", ram, ram_limit)
        draw_bar("DISK", disk, disk_limit)
        print("-" * 46)
        check_alerts(cpu, ram, disk)

 #save snapshot to log
        save_to_log(cpu, ram, disk)

# bonus: email if any alert fires and email is enabled
        if use_email:
            alerts = []
            if cpu > cpu_limit:
                alerts.append(f"CPU: {cpu}%")
            if ram > ram_limit:
                alerts.append(f"RAM: {ram}%")
            if disk > disk_limit:
                alerts.append(f"DISK: {disk}%")
            if alerts:
                body = "High usage detected:\n" + "\n".join(alerts)
                send_email_alert(
                    "System Alert!", body,
                    email_info["to"], email_info["from"], email_info["pass"]
                )

        # ── bonus: desktop notification on alert ──
        if cpu > cpu_limit or ram > ram_limit or disk > disk_limit:
            send_desktop_notification("System Alert", "High resource usage detected!")

        time.sleep(interval)

# show last 10 log entries from csv
def view_logs():
    if not os.path.exists(log_file):
        print("  No log file found yet.")
        return
    with open(log_file, "r") as f:
        rows = list(csv.reader(f))
    print("\n  Last 10 log entries:")
    print("  " + "  |  ".join(rows[0]))
    print("  " + "-" * 50)
    for row in rows[-10:]:
        if row != rows[0]:
            print("  " + "  |  ".join(row))
    print()

#let user update alert thresholds
def set_thresholds():
    global cpu_limit, ram_limit, disk_limit
    print(f"\n  Current -> CPU: {cpu_limit}%  RAM: {ram_limit}%  Disk: {disk_limit}%")
    try:
        cpu_limit  = int(input("  New CPU  threshold (press Enter to skip): ") or cpu_limit)
        ram_limit  = int(input("  New RAM  threshold (press Enter to skip): ") or ram_limit)
        disk_limit = int(input("  New Disk threshold (press Enter to skip): ") or disk_limit)
        print("  Thresholds updated!")
    except ValueError:
        print("  Invalid input, keeping old values.")

# main menu
def main():
    global keep_running
    setup_log()

 #ask once if user wants email alerts
    use_email = False
    email_info = {}
    want_email = input("Enable email alerts? (y/n): ").strip().lower()
    if want_email == "y":
        email_info["from"] = input("  Your Gmail address: ").strip()
        email_info["pass"] = input("  App password: ").strip()
        email_info["to"]   = input("  Alert recipient email: ").strip()
        use_email = True

    while True:
        print("\n" + "=" * 40)
        print("  SYSTEM MONITOR MENU")
        print("=" * 40)
        print("  1. Start Monitoring")
        print("  2. Set Thresholds")
        print("  3. View Logs")
        print("  4. Exit")
        print("-" * 40)
        choice = input("  Choose (1-4): ").strip()

        if choice == "1":
            if keep_running:
                print("  Already running!")
                continue
            try:
                interval = int(input("  Update interval in seconds (default 3): ") or 3)
            except ValueError:
                interval = 3
            keep_running = True
            # ── run monitor in separate thread so menu stays usable ──
            t = threading.Thread(target=monitor_loop, args=(interval, use_email, email_info), daemon=True)
            t.start()
            input("  Press Enter to return to menu...\n")
            keep_running = False

        elif choice == "2":
            set_thresholds()

        elif choice == "3":
            view_logs()

        elif choice == "4":
            keep_running = False
            print("  Goodbye! Stay resourceful :)\n")
            break

        else:
            print("  Invalid choice, try again.")

if __name__ == "__main__":
    main()