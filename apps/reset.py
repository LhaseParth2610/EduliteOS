import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def reset_system():
    confirm = messagebox.askyesno(
        "Confirm Reset",
        "Reset Edulite OS to its original state?\n\nThis will delete all user data."
    )
    if confirm:
        messagebox.showinfo("Reset Success", "System would now reset and reboot (simulated).")
    else:
        messagebox.showinfo("Reset Cancelled", "No changes were made.")

# Initialize main window
root = tk.Tk()
root.title("EduReset - Restore OS")
root.geometry("420x250")
root.configure(bg="#f6f6f6")
root.resizable(False, False)

# Ubuntu-style fonts and color
FONT_HEADER = ("Ubuntu", 16, "bold")
FONT_BODY = ("Ubuntu", 11)
ACCENT_COLOR = "#E95420"  # Ubuntu orange

# Header Label
title = tk.Label(
    root,
    text="🛠 EduReset",
    font=FONT_HEADER,
    fg="#333",
    bg="#f6f6f6"
)
title.pack(pady=(20, 5))

# Sub-description
subtitle = tk.Label(
    root,
    text="Reset your Edulite OS to factory state.\nIdeal for shared lab environments.",
    font=FONT_BODY,
    fg="#555",
    bg="#f6f6f6",
    justify="center"
)
subtitle.pack(pady=(0, 15))

# Reset Button (Ubuntu orange)
reset_btn = tk.Button(
    root,
    text="Reset to Factory Settings",
    font=("Ubuntu", 11, "bold"),
    bg=ACCENT_COLOR,
    fg="white",
    activebackground="#cf4b1e",
    activeforeground="white",
    padx=15,
    pady=8,
    bd=0,
    relief="flat",
    command=reset_system
)
reset_btn.pack(pady=10)

# Warning
warning = tk.Label(
    root,
    text="⚠ This will remove user data.",
    font=("Ubuntu", 10),
    fg="#b00020",
    bg="#f6f6f6"
)
warning.pack(pady=(20, 10))

# Run GUI loop
root.mainloop()
