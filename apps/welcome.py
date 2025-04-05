#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

# Define pages with content and corresponding icons
pages = [
    {
        "title": "Welcome to EduLite OS",
        "content": "A lightweight OS designed for education.\nSimple. Powerful. Resource-efficient.",
        "icon": "welcome"
    },
    {
        "title": "Boot Instructions",
        "content": "• Insert USB drive\n• Restart computer\n• Press F2/F12/Del for BIOS\n• Select USB from boot options",
        "icon": "boot"
    },
    {
        "title": "Mode Selection",
        "content": "• Live Mode: Try without installing\n• Install Mode: Full installation\n\nLive Mode ideal for first-time users.",
        "icon": "mode"
    },
    {
        "title": "Offline Features",
        "content": "Works offline with preloaded tools:\n• TuxMath\n• LibreOffice\n• Educational games\n• Programming tools",
        "icon": "offline"
    },
    {
        "title": "Getting Started",
        "content": "• Login: student\n• Password: student\n\nFind learning tools in the Education menu.",
        "icon": "start"
    },
    {
        "title": "Finish & Explore!",
        "content": "You're all set to begin your learning journey!\n\nThe Help icon can bring you back to this guide anytime.",
        "icon": "finish"
    }
]

# Colors
COLORS = {
    "bg": "#f5f5f5",
    "fg": "#333333",
    "accent": "#4285f4",
    "button_bg": "#ffffff",
    "button_fg": "#333333",
    "button_hover": "#e0e0e0",
    "dot_active": "#4285f4",
    "dot_inactive": "#c0c0c0"
}

# Set up icon paths - fallback to letter icons if images not found
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(ICON_FOLDER, exist_ok=True)

# Main window
window = tk.Tk()
window.title("EduLite OS Welcome")
window.geometry("700x500")
window.configure(bg=COLORS["bg"])
window.resizable(False, False)

# Icon placeholder function - creates a text-based icon if image not found
def get_icon(name, size=64):
    icon_path = os.path.join(ICON_FOLDER, f"{name}.png")
    
    try:
        if os.path.exists(icon_path):
            img = Image.open(icon_path)
            img = img.resize((size, size), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            # Fallback: Create text-based icon
            return None
    except Exception:
        return None

# Create a frame for the entire content
main_frame = tk.Frame(window, bg=COLORS["bg"], padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Header with title
header_frame = tk.Frame(main_frame, bg=COLORS["bg"])
header_frame.pack(fill=tk.X, pady=(0, 20))

title_label = tk.Label(
    header_frame, 
    text="Welcome to EduLite OS", 
    font=("Helvetica", 18, "bold"),
    fg=COLORS["accent"],
    bg=COLORS["bg"]
)
title_label.pack()

# Progress dots
dots_frame = tk.Frame(main_frame, bg=COLORS["bg"])
dots_frame.pack(fill=tk.X, pady=(0, 20))

dots = []
for i in range(len(pages)):
    dot = tk.Label(
        dots_frame, 
        text="●", 
        fg=COLORS["dot_active"] if i == 0 else COLORS["dot_inactive"], 
        bg=COLORS["bg"],
        font=("Helvetica", 12)
    )
    dot.pack(side=tk.LEFT, padx=5)
    dots.append(dot)

# Content area
content_frame = tk.Frame(main_frame, bg=COLORS["bg"], pady=20)
content_frame.pack(fill=tk.BOTH, expand=True)

# Icon display
icon_frame = tk.Frame(content_frame, bg=COLORS["bg"])
icon_frame.pack(pady=(0, 20))

icon_label = tk.Label(icon_frame, bg=COLORS["bg"])
icon_label.pack()

# Text content
text_frame = tk.Frame(content_frame, bg=COLORS["bg"])
text_frame.pack(fill=tk.BOTH, expand=True)

page_title = tk.Label(
    text_frame, 
    font=("Helvetica", 14, "bold"),
    fg=COLORS["fg"],
    bg=COLORS["bg"],
    justify="center"
)
page_title.pack(pady=(0, 10))

page_content = tk.Label(
    text_frame, 
    font=("Helvetica", 12),
    fg=COLORS["fg"],
    bg=COLORS["bg"],
    justify="center",
    wraplength=500
)
page_content.pack()

# Navigation buttons
button_frame = tk.Frame(main_frame, bg=COLORS["bg"], pady=20)
button_frame.pack(fill=tk.X)

# Button styling
button_style = {
    "font": ("Helvetica", 10),
    "bg": COLORS["button_bg"],
    "fg": COLORS["button_fg"],
    "padx": 15,
    "pady": 8,
    "relief": tk.FLAT,
    "borderwidth": 1
}

prev_button = tk.Button(
    button_frame, 
    text="Back",
    **button_style
)
prev_button.pack(side=tk.LEFT, padx=5)

skip_button = tk.Button(
    button_frame, 
    text="Skip",
    **button_style
)
skip_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(
    button_frame, 
    text="Next",
    **button_style
)
next_button.pack(side=tk.RIGHT, padx=5)

finish_button = tk.Button(
    button_frame, 
    text="Finish",
    **button_style
)
finish_button.pack(side=tk.RIGHT, padx=5)

# Create hover effects for buttons
def on_enter(e):
    e.widget['background'] = COLORS["button_hover"]

def on_leave(e):
    e.widget['background'] = COLORS["button_bg"]

for btn in [prev_button, next_button, skip_button, finish_button]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Page tracker
page_num = 0

# Letter icons as fallback
letter_icons = {}
def create_letter_icon(letter, size=64):
    canvas = tk.Canvas(icon_frame, width=size, height=size, bg=COLORS["bg"], highlightthickness=0)
    circle = canvas.create_oval(2, 2, size-2, size-2, fill=COLORS["accent"], outline="")
    canvas.create_text(size/2, size/2, text=letter, fill="white", font=("Helvetica", int(size/2), "bold"))
    return canvas

# Navigation functions
def next_page():
    global page_num
    if page_num < len(pages) - 1:
        page_num += 1
        update_display()

def prev_page():
    global page_num
    if page_num > 0:
        page_num -= 1
        update_display()

def skip_tutorial():
    if messagebox.askyesno("Skip Tutorial", "Are you sure you want to skip the welcome guide?"):
        window.quit()

def finish_tutorial():
    messagebox.showinfo("Welcome Complete", "Welcome to EduLite OS! Enjoy your learning journey.")
    window.quit()

def update_display():
    # Update title at the top
    title_label.config(text=f"Welcome to EduLite OS ({page_num+1}/{len(pages)})")
    
    # Update page content
    current_page = pages[page_num]
    page_title.config(text=current_page["title"])
    page_content.config(text=current_page["content"])
    
    # Update icon
    for widget in icon_frame.winfo_children():
        widget.destroy()
        
    icon = get_icon(current_page["icon"])
    if icon:
        icon_lbl = tk.Label(icon_frame, image=icon, bg=COLORS["bg"])
        icon_lbl.image = icon  # Keep a reference
    else:
        # Fallback to letter icon
        letter = current_page["title"][0]
        canvas = create_letter_icon(letter)
        canvas.pack()
    
    # Update dots
    for i, dot in enumerate(dots):
        dot.config(fg=COLORS["dot_active"] if i == page_num else COLORS["dot_inactive"])
    
    # Update buttons
    prev_button.pack(side=tk.LEFT, padx=5) if page_num > 0 else prev_button.pack_forget()
    next_button.pack(side=tk.RIGHT, padx=5) if page_num < len(pages) - 1 else next_button.pack_forget()
    finish_button.pack(side=tk.RIGHT, padx=5) if page_num == len(pages) - 1 else finish_button.pack_forget()

# Connect button commands
prev_button.config(command=prev_page)
next_button.config(command=next_page)
skip_button.config(command=skip_tutorial)
finish_button.config(command=finish_tutorial)

# Initial update
update_display()

# Center window on screen
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

window.mainloop()