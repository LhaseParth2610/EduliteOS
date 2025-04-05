import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Lab Mode Control")
root.geometry("400x250")
root.configure(bg="#f6f6f6")  # Ubuntu light gray background
root.resizable(False, False)

# Ubuntu-style fonts and colors
FONT_HEADER = ("Ubuntu", 16, "bold")
FONT_BODY = ("Ubuntu", 11)
FONT_INFO = ("Ubuntu", 10)
ACCENT_COLOR = "#E95420"  # Ubuntu orange
TEXT_COLOR = "#333333"    # Dark gray for text
BG_COLOR = "#f6f6f6"      # Background color

# Style configuration for ttk widgets
style = ttk.Style()
style.theme_use("clam")  # Clean, flat theme
style.configure(
    "Custom.TButton",
    font=("Ubuntu", 11, "bold"),
    background=ACCENT_COLOR,
    foreground="white",
    borderwidth=0,
    padding=8,
    relief="flat"
)
style.map(
    "Custom.TButton",
    background=[("active", "#CF4B1E"), ("disabled", "#AEA79F")],
    foreground=[("active", "white")]
)

# Simulated state
lab_mode_active = False

# Toggle Lab Mode (UI only)
def toggle_lab_mode():
    global lab_mode_active
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return
    
    if lab_mode_active:
        # Simulate deactivation
        confirm = messagebox.askyesno("Confirm", "Deactivate Lab Mode?")
        if confirm:
            lab_mode_active = False
            update_ui()
            messagebox.showinfo("Success", "Lab Mode deactivated (simulated).")
        else:
            messagebox.showinfo("Cancelled", "No changes made.")
    else:
        # Simulate activation
        confirm = messagebox.askyesno("Confirm", "Activate Lab Mode?")
        if confirm:
            lab_mode_active = True
            update_ui()
            messagebox.showinfo("Success", "Lab Mode activated (simulated).")
        else:
            messagebox.showinfo("Cancelled", "No changes made.")
    password_entry.delete(0, tk.END)

# Update UI based on Lab Mode state
def update_ui():
    if lab_mode_active:
        status_label.config(text="Lab Mode: Active", fg="red")
        action_button.config(text="Deactivate Lab Mode")
        timer_label.config(text="Time remaining: 02:00")  # Static placeholder
    else:
        status_label.config(text="Lab Mode: Inactive", fg="green")
        action_button.config(text="Activate Lab Mode")
        timer_label.config(text="")  # Clear timer when inactive

# Header Label
title = tk.Label(
    root,
    text="🔬 Lab Mode",
    font=FONT_HEADER,
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
title.pack(pady=(20, 5))

# Status Label
status_label = tk.Label(
    root,
    text="Lab Mode: Inactive",
    font=FONT_BODY,
    fg="green",
    bg=BG_COLOR
)
status_label.pack(pady=5)

# Password Entry Frame
password_frame = tk.Frame(root, bg=BG_COLOR)
password_frame.pack(pady=10)
tk.Label(
    password_frame,
    text="Password:",
    font=FONT_BODY,
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(side="left", padx=5)
password_entry = tk.Entry(
    password_frame,
    show="*",
    font=FONT_BODY,
    width=20
)
password_entry.pack(side="left", padx=5)

# Action Button
action_button = ttk.Button(
    root,
    text="Activate Lab Mode",
    style="Custom.TButton",
    command=toggle_lab_mode,
    cursor="hand2"
)
action_button.pack(pady=10)

# Timer Label (static placeholder)
timer_label = tk.Label(
    root,
    text="",
    font=FONT_INFO,
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
timer_label.pack(pady=5)

# Info Label
info_label = tk.Label(
    root,
    text="Enter password to activate/deactivate Lab Mode.",
    font=FONT_INFO,
    fg="#555555",
    bg=BG_COLOR
)
info_label.pack(pady=5)

# Initial UI setup
update_ui()

# Run GUI loop
root.mainloop()