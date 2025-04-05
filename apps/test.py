import customtkinter as ctk
import os
import json
import time
import threading
from tkinter import messagebox
import hashlib

# Config
TEST_DIR = "tests"
CONFIG = {
    "password": hashlib.sha256("exam123".encode()).hexdigest(),
    "exam_duration": 300  # 5 minutes
}
exam_mode_active = False
monitoring_running = False
end_time = 0
current_question = 0
student_answers = {}
test_data = None
LOG_FILE = "exam_mode_simulation.log"

# GUI Setup
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Student Exam Portal")
root.geometry("650x550")
root.resizable(False, False)
root.configure(fg_color="#F0F0F0")

# Log
def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {msg}\n")
    print(msg)

# Process Monitoring Simulation
def process_monitor():
    while monitoring_running:
        log("Monitoring processes... Simulating kill of unauthorized apps")
        time.sleep(5)

def start_process_monitor():
    global monitoring_running
    monitoring_running = True
    threading.Thread(target=process_monitor, daemon=True).start()

def stop_process_monitor():
    global monitoring_running
    monitoring_running = False

# Load Tests
def load_tests():
    return [f for f in os.listdir(TEST_DIR) if f.endswith(".json")]

# --- App Logic ---
def start_exam_from_file(file):
    global test_data, current_question, student_answers, exam_mode_active, end_time

    with open(os.path.join(TEST_DIR, file), "r") as f:
        test_data = json.load(f)

    current_question = 0
    student_answers = {i: None for i in range(len(test_data["questions"]))}
    end_time = time.time() + CONFIG["exam_duration"]
    exam_mode_active = True
    start_process_monitor()
    show_exam_ui()
    update_timer()
    display_question()

# GUI Screens
def show_exam_ui():
    selection_frame.pack_forget()
    exam_frame.pack(fill="both", expand=True)

def show_selection_ui():
    exam_frame.pack_forget()
    selection_frame.pack(fill="both", expand=True)

# --- UI Events ---
def submit_exam():
    stop_process_monitor()
    global exam_mode_active
    exam_mode_active = False
    score = sum(1 for i, ans in student_answers.items() if ans == test_data["questions"][i]["correct"])
    messagebox.showinfo("Exam Completed", f"Your score: {score}/{len(test_data['questions'])}")
    show_selection_ui()

def quit_exam():
    if messagebox.askyesno("Quit", "Are you sure you want to quit the exam?"):
        stop_process_monitor()
        show_selection_ui()

def save_answer():
    for i, var in enumerate(option_vars):
        if var.get():
            student_answers[current_question] = i
            return

def next_question():
    global current_question
    save_answer()
    if current_question < len(test_data["questions"]) - 1:
        current_question += 1
        display_question()

def prev_question():
    global current_question
    save_answer()
    if current_question > 0:
        current_question -= 1
        display_question()

def display_question():
    question = test_data["questions"][current_question]
    question_label.configure(text=f"Q{current_question+1}: {question['text']}")
    for i, opt in enumerate(question["options"]):
        option_checkboxes[i].configure(text=opt)
        option_vars[i].set(student_answers[current_question] == i)

def update_timer():
    if exam_mode_active:
        remaining = end_time - time.time()
        if remaining > 0:
            m, s = divmod(int(remaining), 60)
            timer_label.configure(text=f"Time Left: {m:02}:{s:02}")
            root.after(1000, update_timer)
        else:
            timer_label.configure(text="Time’s up!")
            submit_exam()

# --- UI Elements ---

# 1. Selection UI
selection_frame = ctk.CTkFrame(root, fg_color="#F0F0F0")
selection_frame.pack(fill="both", expand=True)

label = ctk.CTkLabel(selection_frame, text="📘 Select Exam", font=("Ubuntu", 20, "bold"))
label.pack(pady=15)

tests = load_tests()
for test in tests:
    ctk.CTkButton(selection_frame, text=test.replace(".json", "").capitalize(),
                  font=("Ubuntu", 14), fg_color="#2C72B4", hover_color="#245B8E",
                  command=lambda t=test: start_exam_from_file(t)).pack(pady=4)

# 2. Exam UI
exam_frame = ctk.CTkFrame(root, fg_color="#F0F0F0")

exam_title = ctk.CTkLabel(exam_frame, text="📝 Exam in Progress", font=("Ubuntu", 20, "bold"))
exam_title.pack(pady=10)

timer_label = ctk.CTkLabel(exam_frame, text="", font=("Ubuntu", 12))
timer_label.pack(pady=5)

question_label = ctk.CTkLabel(exam_frame, text="Question will appear here", font=("Ubuntu", 14), wraplength=550)
question_label.pack(pady=10)

option_vars = [ctk.BooleanVar() for _ in range(4)]
option_checkboxes = []
for i in range(4):
    cb = ctk.CTkCheckBox(exam_frame, text="", variable=option_vars[i],
                         command=lambda i=i: [v.set(0) for j, v in enumerate(option_vars) if j != i],
                         font=("Ubuntu", 12))
    cb.pack(anchor="w", padx=20, pady=2)
    option_checkboxes.append(cb)

nav_frame = ctk.CTkFrame(exam_frame, fg_color="#F0F0F0")
nav_frame.pack(pady=10)

ctk.CTkButton(nav_frame, text="Previous", command=prev_question).pack(side="left", padx=5)
ctk.CTkButton(nav_frame, text="Next", command=next_question).pack(side="left", padx=5)
ctk.CTkButton(nav_frame, text="Submit", fg_color="#FF5555", hover_color="#CC4444", command=submit_exam).pack(side="left", padx=5)
ctk.CTkButton(nav_frame, text="Quit", fg_color="#999999", hover_color="#777777", command=quit_exam).pack(side="left", padx=5)

# Start App
show_selection_ui()
root.mainloop()
