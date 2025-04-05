import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def reset_system():
    confirm = messagebox.askyesno(
        "Confirm Reset",
        "Reset Edulite OS to its original state?\n\nThis will delete all user data and reboot the system.",
        icon="warning"
    )
    if confirm:
        messagebox.showinfo("Reset Success", "System would now reset and reboot (simulated).")
    else:
        messagebox.showinfo("Reset Cancelled", "No changes were made.")

# Initialize main window
root = tk.Tk()
root.title("EduReset - Restore OS")
root.geometry("420x250")
root.configure(bg="#F0F0F0")  # Warm grayish background similar to Ubuntu
root.resizable(False, False)

# Ubuntu-style fonts and colors
FONT_HEADER = ("Ubuntu", 16, "bold")
FONT_BODY = ("Ubuntu", 11)
FONT_WARNING = ("Ubuntu", 10)
ACCENT_COLOR = "#E95420"  # Ubuntu orange
TEXT_COLOR = "#333333"    # Dark gray for text
BG_COLOR = "#F0F0F0"      # Light background
WARNING_COLOR = "#B00020" # Ubuntu red for warnings

# Style configuration for ttk widgets
style = ttk.Style()
style.theme_use("clam")  # Use 'clam' theme for a cleaner look
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

# Header Frame
header_frame = tk.Frame(root, bg=BG_COLOR)
header_frame.pack(pady=(20, 10), fill="x")

title = tk.Label(
    header_frame,
    text="🛠 EduReset",
    font=FONT_HEADER,
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
title.pack()

# Subtitle
subtitle = tk.Label(
    root,
    text="Reset your Edulite OS to factory state.\nIdeal for shared lab environments.",
    font=FONT_BODY,
    fg="#555555",  # Slightly lighter gray for contrast
    bg=BG_COLOR,
    justify="center"
)
subtitle.pack(pady=(0, 20))

# Reset Button (using ttk for better theming)
reset_btn = ttk.Button(
    root,
    text="Reset to Factory Settings",
    style="Custom.TButton",
    command=reset_system,
    cursor="hand2"  # Hand cursor for better UX
)
reset_btn.pack(pady=10)

# Warning Label
warning = tk.Label(
    root,
    text="⚠ This will remove all user data and settings.",
    font=FONT_WARNING,
    fg=WARNING_COLOR,
    bg=BG_COLOR
)
warning.pack(pady=(20, 10))

# Run GUI loop
root.mainloop()