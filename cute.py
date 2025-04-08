import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import requests
import re
import os

# --- Basic Vulnerability Scanner ---
def sqli_scanner(url):
    payloads = ["'", "\"", "'--", "\"--", "' OR '1'='1", "\" OR \"1\"=\"1"]
    found = False
    for payload in payloads:
        try:
            r = requests.get(url + payload, timeout=5)
            if re.search("SQL syntax|sql error|mysql_fetch|mysqli|syntax error", r.text, re.I):
                log_result(f"[SQLi] Vulnerable: {url + payload}")
                found = True
                break
        except Exception as e:
            continue
    if not found:
        log_result(f"[SQLi] Not vulnerable: {url}")

def xss_scanner(url):
    payload = "<script>alert(1)</script>"
    try:
        r = requests.get(url + payload, timeout=5)
        if payload in r.text:
            log_result(f"[XSS] Vulnerable: {url + payload}")
        else:
            log_result(f"[XSS] Not vulnerable: {url}")
    except:
        pass

def shell_upload_checker(url):
    keywords = ["shell", "cmd", "wso", "b374k", "upl0ad"]
    try:
        r = requests.get(url, timeout=5)
        for key in keywords:
            if key in r.text.lower():
                log_result(f"[Shell] Possible shell found: {url}")
                return
        log_result(f"[Shell] Not detected: {url}")
    except:
        pass

# --- Thread wrapper ---
def scan_thread(url, vuln_type):
    if vuln_type == "SQLi":
        sqli_scanner(url)
    elif vuln_type == "XSS":
        xss_scanner(url)
    elif vuln_type == "Shell":
        shell_upload_checker(url)

# --- GUI Functions ---
def start_scan():
    urls = input_box.get("1.0", tk.END).strip().split("\n")
    vuln_type = vuln_type_var.get()
    for url in urls:
        if url:
            threading.Thread(target=scan_thread, args=(url.strip(), vuln_type)).start()

def log_result(text):
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)
    with open("scan_results.txt", "a") as f:
        f.write(text + "\n")

# --- GUI ---
app = tk.Tk()
app.title("VULNEX GUI Edition")
app.geometry("650x500")

frame_top = tk.Frame(app)
frame_top.pack(pady=10)

vuln_type_var = tk.StringVar(value="SQLi")
vuln_menu = tk.OptionMenu(frame_top, vuln_type_var, "SQLi", "XSS", "Shell")
vuln_menu.pack(side=tk.LEFT, padx=5)

scan_btn = tk.Button(frame_top, text="Start Scan", command=start_scan)
scan_btn.pack(side=tk.LEFT, padx=5)

input_box = scrolledtext.ScrolledText(app, height=10)
input_box.pack(fill=tk.BOTH, padx=10, pady=5)

output_box = scrolledtext.ScrolledText(app, height=15)
output_box.pack(fill=tk.BOTH, padx=10, pady=5)

app.mainloop()
