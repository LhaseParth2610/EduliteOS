import customtkinter as ctk
import time
import threading
import os
import hashlib
from tkinter import messagebox

# Simulated state variables
exam_mode_active = False
end_time = 0
monitoring_running = False
LOG_FILE = "exam_mode_simulation.log"  # Temporary log file for simulation

# Simulated configuration
CONFIG = {
    "password": hashlib.sha256("exam123".encode()).hexdigest(),  # Default password: "exam123"
    "exam_duration": 120  # 2 minutes in seconds for testing
}

# Log simulation actions (safe, just writes to a file and console)
def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {message}\n")
    print(f"SIMULATION: {message}")

# Simulated exam mode activation (no real changes, just logs)
def activate_exam_mode():
    global end_time
    log_action("Activating Exam Mode...")
    log_action("Simulating: Setting fullscreen and locking window focus")
    log_action("Simulating: Blocking keyboard shortcuts (Alt+Tab, Ctrl+Alt+Del)")
    log_action("Simulating: Restricting processes to exam app only")
    start_process_monitor()
    if CONFIG["exam_duration"] > 0:
        end_time = time.time() + CONFIG["exam_duration"]
        threading.Timer(CONFIG["exam_duration"], lambda: root.after(0, auto_exit)).start()
        update_timer()

# Simulated exam mode deactivation (no real changes, just logs)
def deactivate_exam_mode():
    log_action("Deactivating Exam Mode...")
    log_action("Simulating: Restoring window state")
    log_action("Simulating: Re-enabling keyboard shortcuts")
    log_action("Simulating: Restoring process access")
    stop_process_monitor()

# Simulated process monitoring (logs every 5 seconds, no actual process killing)
def process_monitor():
    while monitoring_running:
        log_action("Monitoring processes... (Allowed: exam_app)")
        log_action("Simulating: Terminating unauthorized process 'firefox'")
        time.sleep(5)

def start_process_monitor():
    global monitoring_running
    monitoring_running = True
    threading.Thread(target=process_monitor, daemon=True).start()

def stop_process_monitor():
    global monitoring_running
    monitoring_running = False

# Toggle Exam Mode
def toggle_exam_mode():
    global exam_mode_active
    password = password_entry.get()
    if hashlib.sha256(password.encode()).hexdigest() != CONFIG["password"]:
        messagebox.showerror("Error", "Incorrect password.")
        return
    
    if exam_mode_active:
        confirm = messagebox.askyesno("Confirm", "Exit Exam Mode?")
        if confirm:
            deactivate_exam_mode()
            exam_mode_active = False
            update_ui()
            messagebox.showinfo("Success", "Exam Mode exited (simulated).")
        else:
            messagebox.showinfo("Cancelled", "Exam continues.")
    else:
        confirm = messagebox.askyesno("Confirm", "Start Exam Mode?")
        if confirm:
            activate_exam_mode()
            exam_mode_active = True
            update_ui()
            messagebox.showinfo("Success", "Exam Mode started (simulated).")
        else:
            messagebox.showinfo("Cancelled", "Exam not started.")
    password_entry.delete(0, "end")

# Auto-exit when time limit is reached
def auto_exit():
    global exam_mode_active
    if exam_mode_active:
        deactivate_exam_mode()
        exam_mode_active = False
        update_ui()
        messagebox.showinfo("Time's Up", "Exam Mode has ended (simulated).")

# Update UI
def update_ui():
    if exam_mode_active:
        status_label.configure(text="Exam Mode: Active", text_color="#FF5555")
        action_button.configure(text="Exit Exam Mode", fg_color="#FF5555", hover_color="#CC4444")
        question_frame.pack(pady=10)
    else:
        status_label.configure(text="Exam Mode: Inactive", text_color="#55AA55")
        action_button.configure(text="Start Exam Mode", fg_color="#E95420", hover_color="#CF4B1E")
        timer_label.configure(text="")
        question_frame.pack_forget()

# Update timer display
def update_timer():
    if exam_mode_active and end_time > 0:
        remaining = end_time - time.time()
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            timer_label.configure(text=f"Time remaining: {mins:02d}:{secs:02d}")
            root.after(1000, update_timer)
        else:
            timer_label.configure(text="")

# Handle window close
def on_closing():
    if exam_mode_active:
        password = password_entry.get()
        if hashlib.sha256(password.encode()).hexdigest() == CONFIG["password"]:
            deactivate_exam_mode()
            root.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password. Cannot exit Exam Mode.")
    else:
        root.destroy()

# Initialize main window
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Exam Mode (Simulation)")
root.geometry("500x400")
root.resizable(False, False)
root.configure(fg_color="#F0F0F0")

# Header Label
title_label = ctk.CTkLabel(
    root,
    text="📝 Exam Mode",
    font=("Ubuntu", 20, "bold"),
    text_color="#333333"
)
title_label.pack(pady=(20, 10))

# Status Label
status_label = ctk.CTkLabel(
    root,
    text="Exam Mode: Inactive",
    font=("Ubuntu", 14),
    text_color="#55AA55"
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
    text="Start Exam Mode",
    font=("Ubuntu", 12, "bold"),
    fg_color="#E95420",
    hover_color="#CF4B1E",
    text_color="white",
    command=toggle_exam_mode,
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

# Exam Question Frame (visible only in Exam Mode)
question_frame = ctk.CTkFrame(root, fg_color="#FFFFFF", corner_radius=10)
ctk.CTkLabel(
    question_frame,
    text="Sample Question: What is 2 + 2?",
    font=("Ubuntu", 12),
    text_color="#333333",
    wraplength=400
).pack(pady=5)
answer_entry = ctk.CTkEntry(
    question_frame,
    font=("Ubuntu", 12),
    width=200,
    placeholder_text="Enter your answer"
)
answer_entry.pack(pady=5)

# Info Label
info_label = ctk.CTkLabel(
    root,
    text="Password: 'exam123' (for simulation)",
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