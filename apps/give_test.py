import customtkinter as ctk
import time
import threading
import os
import hashlib
import json
from tkinter import messagebox

# Simulated state variables
exam_mode_active = False
end_time = 0
monitoring_running = False
LOG_FILE = "exam_mode_simulation.log"
TEST_FILE = "simulated_test.json"
current_question = 0
student_answers = {}
test_data = None

# Simulated configuration
CONFIG = {
    "password": hashlib.sha256("exam123".encode()).hexdigest(),  # Default password: "exam123"
    "exam_duration": 120  # 2 minutes for display only
}

# Log simulation actions (safe, just writes to a file and console)
def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {message}\n")
    print(f"SIMULATION: {message}")

# Simulated exam mode activation
def activate_exam_mode():
    global end_time, test_data, exam_mode_active
    if not os.path.exists(TEST_FILE):
        messagebox.showerror("Error", "No test file found. Please create a test first.")
        return False
    log_action("Activating Exam Mode...")
    log_action("Simulating: Setting fullscreen and locking window focus")
    log_action("Simulating: Blocking keyboard shortcuts (Alt+Tab, Ctrl+Alt+Del)")
    log_action("Simulating: Restricting processes to exam app only")
    start_process_monitor()
    with open(TEST_FILE, "r") as f:
        test_data = json.load(f)
    load_test()
    end_time = time.time() + CONFIG["exam_duration"]  # For timer display only
    exam_mode_active = True
    update_timer()
    return True

# Simulated exam mode deactivation
def deactivate_exam_mode():
    global exam_mode_active
    log_action("Deactivating Exam Mode...")
    log_action("Simulating: Restoring window state")
    log_action("Simulating: Re-enabling keyboard shortcuts")
    log_action("Simulating: Restoring process access")
    stop_process_monitor()
    exam_mode_active = False

# Simulated process monitoring
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

# Load test from file (simulated)
def load_test():
    global current_question, student_answers
    current_question = 0
    student_answers = {i: None for i in range(len(test_data["questions"]))}
    display_question()

# Display current question
def display_question():
    question = test_data["questions"][current_question]
    question_label.configure(text=f"Q{current_question + 1}/{len(test_data['questions'])}: {question['text']}")
    for i, (checkbox, var) in enumerate(zip(option_checkboxes, option_vars)):
        checkbox.configure(text=question["options"][i])
        var.set(0)  # Reset checkbox state
        if student_answers[current_question] == i:
            var.set(1)  # Restore previous answer
    update_navigation()

# Update navigation buttons
def update_navigation():
    prev_button.configure(state="normal" if current_question > 0 else "disabled")
    next_button.configure(state="normal" if current_question < len(test_data["questions"]) - 1 else "disabled")
    if current_question == len(test_data["questions"]) - 1:
        submit_button.pack(side="right", padx=5)
    else:
        submit_button.pack_forget()

# Move to previous question
def prev_question():
    global current_question
    save_current_answer()
    current_question -= 1
    display_question()

# Save answer and move to next question
def answer_and_next():
    global current_question
    save_current_answer()
    if current_question < len(test_data["questions"]) - 1:
        current_question += 1
        display_question()
    else:
        confirm_submit()

# Save current answer
def save_current_answer():
    for i, var in enumerate(option_vars):
        if var.get():
            student_answers[current_question] = i
            break
    else:
        student_answers[current_question] = None

# Confirm submission after last question
def confirm_submit():
    if messagebox.askyesno("Submit Exam", "You’ve reached the last question. Submit your exam now?"):
        submit_exam()
    else:
        messagebox.showinfo("Continue", "You can still review or quit the exam.")

# Submit exam and show score
def submit_exam():
    global exam_mode_active
    save_current_answer()
    deactivate_exam_mode()
    score = sum(1 for i, answer in student_answers.items() if answer is not None and answer == test_data["questions"][i]["correct"])
    total_questions = len(test_data["questions"])
    log_action(f"Simulating: Saving student answers {student_answers}")
    log_action(f"Score: {score}/{total_questions}")
    exam_mode_active = False
    update_ui()
    messagebox.showinfo("Exam Results", f"Exam Submitted!\nScore: {score}/{total_questions}")
    root.quit()

# Quit exam without submitting
def quit_exam():
    global exam_mode_active
    if messagebox.askyesno("Quit Exam", "Are you sure you want to quit? Your progress will be saved, but you can’t resume."):
        save_current_answer()
        deactivate_exam_mode()
        score = sum(1 for i, answer in student_answers.items() if answer is not None and answer == test_data["questions"][i]["correct"])
        total_questions = len(test_data["questions"])
        log_action(f"Simulating: Saving student answers {student_answers}")
        log_action(f"Score: {score}/{total_questions}")
        exam_mode_active = False
        update_ui()
        messagebox.showinfo("Exam Quit", f"Exam Ended!\nScore: {score}/{total_questions}")
        root.quit()

# Start exam after password
def start_exam():
    password = password_entry.get()
    if hashlib.sha256(password.encode()).hexdigest() != CONFIG["password"]:
        messagebox.showerror("Error", "Incorrect password.")
        return
    if activate_exam_mode():
        initial_frame.pack_forget()  # Hide password UI
        exam_frame.pack(fill="both", expand=True)  # Show exam UI

# Update UI based on exam state
def update_ui():
    if exam_mode_active:
        exam_frame.pack(fill="both", expand=True)
        initial_frame.pack_forget()
    else:
        initial_frame.pack(fill="both", expand=True)
        exam_frame.pack_forget()

# Update Timer (display only)
def update_timer():
    if exam_mode_active and end_time > 0:
        remaining = end_time - time.time()
        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            timer_label.configure(text=f"Time remaining: {mins:02d}:{secs:02d}")
            root.after(1000, update_timer)
        else:
            timer_label.configure(text="Time's up! Submit or quit your exam.")

# Initialize main window
ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Student: Take Exam (Simulation)")
root.geometry("600x500")
root.resizable(False, False)
root.configure(fg_color="#F0F0F0")

# Initial Frame (Password Entry)
initial_frame = ctk.CTkFrame(root, fg_color="#F0F0F0")
initial_frame.pack(fill="both", expand=True)

title_label = ctk.CTkLabel(initial_frame, text="📝 Exam Mode", font=("Ubuntu", 20, "bold"), text_color="#333333")
title_label.pack(pady=(50, 10))

password_frame = ctk.CTkFrame(initial_frame, fg_color="#F0F0F0")
password_frame.pack(pady=15)
ctk.CTkLabel(password_frame, text="Password:", font=("Ubuntu", 12), text_color="#333333").pack(side="left", padx=5)
password_entry = ctk.CTkEntry(password_frame, show="*", font=("Ubuntu", 12), width=150, placeholder_text="Enter password")
password_entry.pack(side="left", padx=5)

start_button = ctk.CTkButton(initial_frame, text="Start Exam", font=("Ubuntu", 12, "bold"), fg_color="#E95420",
                             hover_color="#CF4B1E", text_color="white", command=start_exam, corner_radius=10, width=200)
start_button.pack(pady=15)

info_label = ctk.CTkLabel(initial_frame, text="Password: 'exam123' (for simulation)", font=("Ubuntu", 10), text_color="#555555")
info_label.pack(pady=5)

# Exam Frame (Hidden until password entered)
exam_frame = ctk.CTkFrame(root, fg_color="#F0F0F0")
exam_title = ctk.CTkLabel(exam_frame, text="📝 Take Exam", font=("Ubuntu", 20, "bold"), text_color="#333333")
exam_title.pack(pady=(20, 10))

timer_label = ctk.CTkLabel(exam_frame, text="", font=("Ubuntu", 12), text_color="#333333")
timer_label.pack(pady=5)

question_frame = ctk.CTkFrame(exam_frame, fg_color="#FFFFFF", corner_radius=10)
question_frame.pack(pady=10)
question_label = ctk.CTkLabel(question_frame, text="No question loaded", font=("Ubuntu", 12), text_color="#333333", wraplength=500)
question_label.pack(pady=5)
option_vars = [ctk.BooleanVar() for _ in range(4)]
option_checkboxes = []
for i in range(4):
    chk = ctk.CTkCheckBox(question_frame, text="", variable=option_vars[i], font=("Ubuntu", 12), text_color="#333333",
                          command=lambda i=i: [var.set(0) for j, var in enumerate(option_vars) if j != i])  # Single selection
    chk.pack(pady=2, padx=10, anchor="w")
    option_checkboxes.append(chk)

answer_button = ctk.CTkButton(question_frame, text="Answer & Next", font=("Ubuntu", 12), fg_color="#E95420",
                              hover_color="#CF4B1E", text_color="white", command=answer_and_next, corner_radius=10)
answer_button.pack(pady=5)

navigation_frame = ctk.CTkFrame(exam_frame, fg_color="#F0F0F0")
navigation_frame.pack(pady=5)
prev_button = ctk.CTkButton(navigation_frame, text="Previous", font=("Ubuntu", 12), fg_color="#AEA79F", command=prev_question)
prev_button.pack(side="left", padx=5)
next_button = ctk.CTkButton(navigation_frame, text="Next", font=("Ubuntu", 12), fg_color="#AEA79F", command=answer_and_next)
next_button.pack(side="left", padx=5)
submit_button = ctk.CTkButton(navigation_frame, text="Submit Exam", font=("Ubuntu", 12), fg_color="#FF5555",
                              hover_color="#CC4444", command=submit_exam)

quit_button = ctk.CTkButton(exam_frame, text="Quit Exam", font=("Ubuntu", 12), fg_color="#AEA79F",
                            hover_color="#8C8C8C", text_color="white", command=quit_exam, corner_radius=10)
quit_button.pack(pady=10)

# Clear log file at start
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Run GUI loop
root.mainloop()