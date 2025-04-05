import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading
import os
import json
import hashlib

# Simulated state variables
lab_mode_active = False
end_time = 0
monitoring_running = False
LOG_FILE = "lab_mode_simulation.log"  # Temporary log file for simulation

# Simulated configuration (normally from /etc/lab_mode_config.json)
CONFIG = {
    "password": hashlib.sha256("labpass".encode()).hexdigest(),  # Default password: "labpass"
    "restrictions": {
        "apps": ["notepad.exe", "python.exe"],  # Simulated allowed apps
        "time_limit": 120  # 2 minutes in seconds for testing
    }
}

# Log simulation actions
def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {message}\n")
    print(f"SIMULATION: {message}")

# Simulated restriction application
def apply_restrictions():
    global end_time
    log_action("Applying restrictions...")
    log_action("Simulating: Blocking internet (iptables rules)")
    log_action("Simulating: Disabling USB storage (modprobe -r usb-storage)")
    log_action("Simulating: Restricting file system (chmod 700 lab_dir)")
    start_process_monitor()
    if CONFIG["restrictions"]["time_limit"] > 0:
        end_time = time.time() + CONFIG["restrictions"]["time_limit"]
        threading.Timer(CONFIG["restrictions"]["time_limit"], lambda: root.after(0, auto_deactivate)).start()
        update_timer()

# Simulated restriction removal
def revert_restrictions():
    log_action("Reverting restrictions...")
    log_action("Simulating: Restoring internet (iptables -F)")
    log_action("Simulating: Enabling USB storage (modprobe usb-storage)")
    log_action("Simulating: Restoring file system (chmod 755 home_dir)")
    stop_process_monitor()

# Simulated process monitoring
def process_monitor():
    while monitoring_running:
        log_action("Monitoring processes... (Allowed: " + ", ".join(CONFIG["restrictions"]["apps"]) + ")")
        # Simulate killing unauthorized processes
        log_action("Simulating: Terminating unauthorized process 'chrome.exe'")
        time.sleep(5)

def start_process_monitor():
    global monitoring_running
    monitoring_running = True
    threading.Thread(target=process_monitor, daemon=True).start()

def stop_process_monitor():
    global monitoring_running
    monitoring_running = False

# Toggle Lab Mode
def toggle_lab_mode():
    global lab_mode_active
    password = password_entry.get()
    if hashlib.sha256(password.encode()).hexdigest() != CONFIG["password"]:
        messagebox.showerror("Error", "Incorrect password.")
        return
    
    if lab_mode_active:
        confirm = messagebox.askyesno("Confirm", "Deactivate Lab Mode?")
        if confirm:
            revert_restrictions()
            lab_mode_active = False
            update_ui()
            messagebox.showinfo("Success", "Lab Mode deactivated (simulated).")
        else:
            messagebox.showinfo("Cancelled", "No changes made.")
    else:
        confirm = messagebox.askyesno("Confirm", "Activate Lab Mode?")
        if confirm:
            apply_restrictions()
            lab_mode_active = True
            update_ui()
            messagebox.showinfo("Success", "Lab Mode activated (simulated).")
        else:
            messagebox.showinfo("Cancelled", "No changes made.")
    password_entry.delete(0, tk.END)

# Auto-deactivate when time limit is reached
def auto_deactivate():
    global lab_mode_active
    if lab_mode_active:
        revert_restrictions()
        lab_mode_active = False
        update_ui()
        messagebox.showinfo("Time's Up", "Lab Mode has been automatically deactivated (simulated).")

# Update UI
def update_ui():
    if lab_mode_active:
        status_label.config(text="Lab Mode: Active", fg="red")
        action_button.config(text="Deactivate Lab Mode")
    else:
        status_label.config(text="Lab Mode: Inactive", fg="green")
        action_button.config(text="Activate Lab Mode")
        timer_label.config(text="")

# Update timer display
def update_timer():
    if lab_mode_active and end_time > 0:
        remaining = end_time - time.time()
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            timer_label.config(text=f"Time remaining: {mins:02d}:{secs:02d}")
            root.after(1000, update_timer)
        else:
            timer_label.config(text="")

# Handle window close
def on_closing():
    if lab_mode_active:
        password = password_entry.get()
        if hashlib.sha256(password.encode()).hexdigest() == CONFIG["password"]:
            revert_restrictions()
            root.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password. Cannot close while Lab Mode is active.")
    else:
        root.destroy()

# Initialize main window
root = tk.Tk()
root.title("Lab Mode Control (Simulation)")
root.geometry("400x250")
root.configure(bg="#f6f6f6")
root.resizable(False, False)

# Ubuntu-style fonts and colors
FONT_HEADER = ("Ubuntu", 16, "bold")
FONT_BODY = ("Ubuntu", 11)
FONT_INFO = ("Ubuntu", 10)
ACCENT_COLOR = "#E95420"  # Ubuntu orange

# Style configuration for ttk widgets
style = ttk.Style()
style.configure("TButton", font=("Ubuntu", 11, "bold"), background=ACCENT_COLOR, foreground="white", padding=8)
style.map("TButton", background=[("active", "#CF4B1E")])

# Header Label
title = tk.Label(root, text="🔬 Lab Mode", font=FONT_HEADER, fg="#333", bg="#f6f6f6")
title.pack(pady=(20, 5))

# Status Label
status_label = tk.Label(root, text="Lab Mode: Inactive", font=FONT_BODY, fg="green", bg="#f6f6f6")
status_label.pack(pady=5)

# Password Entry
password_frame = tk.Frame(root, bg="#f6f6f6")
password_frame.pack(pady=10)
tk.Label(password_frame, text="Password:", font=FONT_BODY, bg="#f6f6f6").pack(side="left", padx=5)
password_entry = tk.Entry(password_frame, show="*", font=FONT_BODY)
password_entry.pack(side="left", padx=5)

# Action Button
action_button = ttk.Button(root, text="Activate Lab Mode", style="TButton", command=toggle_lab_mode)
action_button.pack(pady=10)

# Timer Label
timer_label = tk.Label(root, text="", font=FONT_INFO, fg="#333", bg="#f6f6f6")
timer_label.pack(pady=5)

# Info Label
info_label = tk.Label(root, text="Password: 'labpass' (for simulation)", font=FONT_INFO, fg="#555", bg="#f6f6f6")
info_label.pack(pady=5)

# Set initial state
update_ui()

# Bind close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Clear log file at start
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Run GUI loop
root.mainloop()