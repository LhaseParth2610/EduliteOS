import customtkinter as ctk
import time
import threading
import os
import hashlib
from tkinter import messagebox

# Simulated state variables
lab_mode_active = False
end_time = 0
monitoring_running = False
LOG_FILE = "lab_mode_simulation.log"  # Temporary log file for simulation

# Simulated configuration
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
    password_entry.delete(0, "end")

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
        status_label.configure(text="Lab Mode: Active", text_color="#FF5555")  # Red for active
        action_button.configure(text="Deactivate Lab Mode", fg_color="#FF5555", hover_color="#CC4444")
    else:
        status_label.configure(text="Lab Mode: Inactive", text_color="#55AA55")  # Green for inactive
        action_button.configure(text="Activate Lab Mode", fg_color="#E95420", hover_color="#CF4B1E")
        timer_label.configure(text="")

# Update timer display
def update_timer():
    if lab_mode_active and end_time > 0:
        remaining = end_time - time.time()
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            timer_label.configure(text=f"Time remaining: {mins:02d}:{secs:02d}")
            root.after(1000, update_timer)
        else:
            timer_label.configure(text="")

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
ctk.set_appearance_mode("light")  # Light theme to match Ubuntu
ctk.set_default_color_theme("dark-blue")  # Base theme (customized below)
root = ctk.CTk()
root.title("Lab Mode Control (Simulation)")
root.geometry("400x300")
root.resizable(False, False)

# Custom styling
root.configure(fg_color="#F0F0F0")  # Ubuntu light gray background

# Header Label
title_label = ctk.CTkLabel(
    root,
    text="🔬 Lab Mode",
    font=("Ubuntu", 20, "bold"),
    text_color="#333333"
)
title_label.pack(pady=(20, 10))

# Status Label
status_label = ctk.CTkLabel(
    root,
    text="Lab Mode: Inactive",
    font=("Ubuntu", 14),
    text_color="#55AA55"  # Green initially
)
status_label.pack(pady=5)

# Password Entry Frame
password_frame = ctk.CTkFrame(root, fg_color="#F0F0F0")
password_frame.pack(pady=15)
ctk.CTkLabel(
    password_frame,
    text="Password:",
    font=("Ubuntu", 12),
    text_color="#333333"
).pack(side="left", padx=5)
password_entry = ctk.CTkEntry(
    password_frame,
    show="*",
    font=("Ubuntu", 12),
    width=150,
    placeholder_text="Enter password",
    fg_color="#FFFFFF",
    text_color="#333333",
    border_color="#AEA79F"
)
password_entry.pack(side="left", padx=5)

# Action Button
action_button = ctk.CTkButton(
    root,
    text="Activate Lab Mode",
    font=("Ubuntu", 12, "bold"),
    fg_color="#E95420",  # Ubuntu orange
    hover_color="#CF4B1E",
    text_color="white",
    command=toggle_lab_mode,
    corner_radius=10,
    width=200
)
action_button.pack(pady=15)

# Timer Label
timer_label = ctk.CTkLabel(
    root,
    text="",
    font=("Ubuntu", 12),
    text_color="#333333"
)
timer_label.pack(pady=5)

# Info Label
info_label = ctk.CTkLabel(
    root,
    text="Password: 'labpass' (for simulation)",
    font=("Ubuntu", 10),
    text_color="#555555"
)
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