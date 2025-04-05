import customtkinter as ctk
import tkinter.messagebox as messagebox
import json
import os
import random
import threading
import time

# ---------- Constants ----------
TEST_FOLDER = "test_jsons"
NUM_TESTS = 10
MAX_FOCUS_LOSSES = 3

# ---------- Global Variables ----------
test_data = {}
student_answers = {}
process_monitor_thread = None
monitor_running = False
focus_loss_count = 0
exam_mode_active = False

# ---------- Setup ----------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Exam Simulation App")
root.geometry("1200x700")

# ---------- Logging ----------
def log(message):
    print("[LOG]", message)

# ---------- Load JSON Tests ----------
def load_test_files():
    return [f for f in os.listdir(TEST_FOLDER) if f.endswith(".json")]

# ---------- Start Exam ----------
def start_exam(filename):
    global test_data, student_answers, focus_loss_count, exam_mode_active
    focus_loss_count = 0
    student_answers.clear()
    exam_mode_active = True

    with open(os.path.join(TEST_FOLDER, filename), "r") as f:
        test_data = json.load(f)

    show_exam_ui()
    load_question(0)
    start_process_monitor()

# ---------- UI: Test Selection ----------
selection_frame = ctk.CTkFrame(root)
selection_frame.pack(fill="both", expand=True)

ctk.CTkLabel(selection_frame, text="Select a Test", font=("Arial", 30)).pack(pady=20)
test_buttons_frame = ctk.CTkFrame(selection_frame)
test_buttons_frame.pack()

def create_test_buttons():
    files = load_test_files()[:NUM_TESTS]
    for idx, f in enumerate(files):
        btn = ctk.CTkButton(test_buttons_frame, text=f"Test {idx+1}", command=lambda file=f: confirm_start(file))
        btn.grid(row=idx//5, column=idx%5, padx=10, pady=10)

def confirm_start(filename):
    if messagebox.askyesno("Confirm", f"Start {filename}?"):
        start_exam(filename)

create_test_buttons()

# ---------- UI: Exam Interface ----------
exam_frame = ctk.CTkFrame(root)

question_label = ctk.CTkLabel(exam_frame, text="", font=("Arial", 20), wraplength=900)
question_label.pack(pady=20)

options_var = ctk.StringVar(value="")
options_buttons = []

def load_question(index):
    for btn in options_buttons:
        btn.destroy()
    options_buttons.clear()

    q = test_data["questions"][index]
    question_label.configure(text=f"Q{index+1}: {q['question']}")
    options_var.set("")

    for i, opt in enumerate(q["options"]):
        btn = ctk.CTkRadioButton(exam_frame, text=opt, variable=options_var, value=opt,
                                 command=lambda idx=index, val=opt: save_answer(idx, val))
        btn.pack(pady=5)
        options_buttons.append(btn)

    update_nav_buttons(index)

def save_answer(q_idx, answer):
    student_answers[q_idx] = answer

# ---------- UI: Navigation ----------
nav_frame = ctk.CTkFrame(exam_frame)
nav_frame.pack(pady=10)
prev_btn = ctk.CTkButton(nav_frame, text="⟵ Prev", command=lambda: navigate(-1))
next_btn = ctk.CTkButton(nav_frame, text="Next ⟶", command=lambda: navigate(1))
submit_btn = ctk.CTkButton(exam_frame, text="✅ Submit Exam", command=lambda: submit_exam())
quit_btn = ctk.CTkButton(exam_frame, text="❌ Quit Exam", command=lambda: quit_exam())

prev_btn.grid(row=0, column=0, padx=10)
next_btn.grid(row=0, column=1, padx=10)
submit_btn.pack(pady=10)
quit_btn.pack()

def navigate(offset):
    current = list(student_answers.keys())[-1] if student_answers else 0
    new_index = current + offset
    if 0 <= new_index < len(test_data["questions"]):
        load_question(new_index)

def update_nav_buttons(index):
    prev_btn.configure(state="normal" if index > 0 else "disabled")
    next_btn.configure(state="normal" if index < len(test_data["questions"])-1 else "disabled")

# ---------- Submit Exam ----------
def submit_exam():
    stop_process_monitor()
    global exam_mode_active
    exam_mode_active = False
    root.attributes("-fullscreen", False)
    score = sum(1 for i, ans in student_answers.items() if ans == test_data["questions"][i]["correct"])
    messagebox.showinfo("Exam Completed", f"Your score: {score}/{len(test_data['questions'])}")
    show_selection_ui()

def quit_exam():
    if messagebox.askyesno("Quit", "Are you sure you want to quit the exam?"):
        stop_process_monitor()
        root.attributes("-fullscreen", False)
        show_selection_ui()

# ---------- Switch Between Frames ----------
def show_exam_ui():
    selection_frame.pack_forget()
    exam_frame.pack(fill="both", expand=True)
    root.attributes("-fullscreen", True)
    root.focus_force()

def show_selection_ui():
    exam_frame.pack_forget()
    selection_frame.pack(fill="both", expand=True)

# ---------- Anti-Cheat: Focus Loss Detection ----------
def on_focus_out(event):
    global focus_loss_count
    if exam_mode_active:
        focus_loss_count += 1
        log(f"Focus lost {focus_loss_count} time(s)")
        messagebox.showwarning("Warning!", f"Focus lost {focus_loss_count} time(s). Max allowed is {MAX_FOCUS_LOSSES}")
        if focus_loss_count >= MAX_FOCUS_LOSSES:
            messagebox.showerror("Exam Terminated", "You switched away too many times. Submitting exam.")
            submit_exam()

root.bind("<FocusOut>", on_focus_out)

# ---------- Anti-Cheat: Disable Right-Click & Screenshot (Simulated) ----------
def block_right_click(event): return "break"
def block_screenshot(event):
    log("Screenshot key pressed!")
    messagebox.showwarning("Anti-Cheat", "Screenshot detected!")

root.bind("<Button-3>", block_right_click)
root.bind("<Print>", block_screenshot)
root.bind("<Control-Shift-s>", block_screenshot)

# ---------- Anti-Cheat: Dummy Monitor Thread ----------
def start_process_monitor():
    global monitor_running, process_monitor_thread
    monitor_running = True
    process_monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    process_monitor_thread.start()

def stop_process_monitor():
    global monitor_running
    monitor_running = False

def monitor_loop():
    while monitor_running:
        # Simulated: You can extend this to detect other apps/processes
        time.sleep(2)

# ---------- Run App ----------
root.mainloop()
