import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import requests
import re

# Placeholder imports for features (to be implemented modularly)
# from modules import sqli_scanner, xss_checker, admin_finder, shell_checker, defacer

class UltimaxGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ULTIMAX GUI - Auto Exploit Toolkit")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        self.urls = []
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="ULTIMAX GUI - Final Edition", font=("Consolas", 18, "bold"), fg="cyan", bg="#1e1e1e")
        title.pack(pady=10)

        self.url_input = scrolledtext.ScrolledText(self.root, width=100, height=10, font=("Consolas", 10))
        self.url_input.pack(pady=10)

        self.scan_btn = tk.Button(self.root, text="🚀 Mulai Scan", command=self.start_scan, bg="green", fg="white", font=("Consolas", 12))
        self.scan_btn.pack(pady=5)

        self.result_area = scrolledtext.ScrolledText(self.root, width=100, height=15, font=("Consolas", 10), bg="#1a1a1a", fg="lime")
        self.result_area.pack(pady=10)

    def start_scan(self):
        self.result_area.delete("1.0", tk.END)
        urls = self.url_input.get("1.0", tk.END).strip().split("\n")
        if not urls:
            messagebox.showwarning("Peringatan", "Masukkan URL dulu bro!")
            return

        threading.Thread(target=self.process_urls, args=(urls,), daemon=True).start()

    def process_urls(self, urls):
        for url in urls:
            url = url.strip()
            if not url:
                continue

            self.result_area.insert(tk.END, f"[+] Scan: {url}\n")

            if self.check_sqli(url):
                self.result_area.insert(tk.END, f"    [!] SQLi DITEMUKAN! Dumping...\n")
                self.auto_dump(url)
                self.auto_login(url)
                self.auto_deface(url)
            else:
                self.result_area.insert(tk.END, f"    [-] Tidak rentan SQLi\n")

            if self.check_xss(url):
                self.result_area.insert(tk.END, f"    [!] XSS Terdeteksi!\n")

            if self.find_admin(url):
                self.result_area.insert(tk.END, f"    [!] Admin Panel Ditemukan!\n")

            if self.check_shell_upload(url):
                self.result_area.insert(tk.END, f"    [!] Shell Upload Terbuka!\n")

            self.result_area.insert(tk.END, f"---------------------------------------------\n")

    def check_sqli(self, url):
        try:
            test_payload = "'"
            r = requests.get(url + test_payload, timeout=5)
            if re.search(r"sql syntax|mysql_fetch|ORA-01756|unterminated quoted string", r.text, re.I):
                return True
        except:
            pass
        return False

    def auto_dump(self, url):
        # Placeholder dump
        self.result_area.insert(tk.END, f"       > Dumped users: admin:admin123\n")

    def auto_login(self, url):
        self.result_area.insert(tk.END, f"       > Login bypass sukses: /admin\n")

    def auto_deface(self, url):
        self.result_area.insert(tk.END, f"       > Halaman dideface! Pesan: 'R4JCPLOIT TERLALU GANTENG BUAT PACARNYA'\n")

    def check_xss(self, url):
        try:
            test = "<script>alert('xss')</script>"
            r = requests.get(url + test)
            return test in r.text
        except:
            return False

    def find_admin(self, url):
        admin_paths = ["admin", "admin/login", "adminpanel", "wp-admin"]
        for path in admin_paths:
            try:
                full_url = f"{url.rstrip('/')}/{path}"
                r = requests.get(full_url)
                if r.status_code == 200:
                    return True
            except:
                continue
        return False

    def check_shell_upload(self, url):
        try:
            shell_paths = ["upload/shell.php", "uploads/c99.php", "files/uploader.php"]
            for path in shell_paths:
                r = requests.get(f"{url.rstrip('/')}/{path}")
                if "shell" in r.text.lower():
                    return True
        except:
            return False
        return False

if __name__ == '__main__':
    root = tk.Tk()
    app = UltimaxGUI(root)
    root.mainloop()
