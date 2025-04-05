import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk, ImageFilter

# Colors for priorities
PRIORITY_COLORS = {
    "High": "#ff4c4c",    # Red
    "Medium": "#f2c94c",  # Yellow
    "Low": "#4ca3ff"      # Blue
}

class ToDoWidget(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.tasks = []
        self.drag_data = {"widget": None, "y": 0}

        # Header
        self.header_label = ctk.CTkLabel(
            self,
            text="📘 My ToDo List",
            font=("Helvetica", 20, "bold"),
            text_color="#4285f4",
            fg_color="white",
            corner_radius=10,
            width=200,
            height=40
        )
        self.header_label.pack(pady=(20, 15))  # Adjusted padding

        # Scrollable Task Frame
        self.task_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="white",
            corner_radius=10,
            width=610,
            height=350
        )
        self.task_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Input Frame
        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#d3d3d3"
        )
        self.input_frame.pack(fill=ctk.X, padx=20, pady=(0, 15))

        self.task_entry = ctk.CTkEntry(
            self.input_frame,
            width=250,
            placeholder_text="Enter task...",
            font=("Helvetica", 14),
            corner_radius=8,
            border_width=0
        )
        self.task_entry.grid(row=0, column=0, padx=15, pady=10, sticky="ew")  # Increased padx

        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_menu = ctk.CTkOptionMenu(
            self.input_frame,
            values=["High", "Medium", "Low"],
            variable=self.priority_var,
            font=("Helvetica", 12),
            dropdown_font=("Helvetica", 12),
            corner_radius=8,
            width=100
        )
        self.priority_menu.grid(row=0, column=1, padx=15, pady=10)  # Increased padx

        self.due_date = DateEntry(
            self.input_frame,
            date_pattern='yyyy-mm-dd',
            font=("Helvetica", 12),
            relief="flat",
            borderwidth=0,
            background="#4285f4",
            foreground="white"
        )
        self.due_date.grid(row=0, column=2, padx=15, pady=10)  # Increased padx

        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="Add Task",
            command=self.add_task,
            font=("Helvetica", 12, "bold"),
            corner_radius=8,
            width=100,
            height=36  # Consistent height
        )
        self.add_button.grid(row=0, column=3, padx=15, pady=10)  # Increased padx

        # Clear Button
        self.clear_btn = ctk.CTkButton(
            self,
            text="Clear All Tasks",
            command=self.clear_all,
            font=("Helvetica", 12, "bold"),
            fg_color="#ff4c4c",
            hover_color="#e04343",
            corner_radius=8,
            width=150,
            height=36  # Consistent height
        )
        self.clear_btn.pack(pady=15)  # Adjusted padding

        # Configure input frame to expand
        self.input_frame.grid_columnconfigure(0, weight=1)

    def add_task(self):
        task_text = self.task_entry.get()
        if not task_text:
            messagebox.showwarning("Input Error", "Task cannot be empty.", parent=self)
            return

        priority = self.priority_var.get()
        due = self.due_date.get_date().strftime("%Y-%m-%d")

        task = ctk.CTkFrame(
            self.task_frame,
            fg_color=PRIORITY_COLORS[priority],
            corner_radius=10,
            border_width=1,
            border_color="#d3d3d3"
        )
        task.pack(fill=ctk.X, pady=5, padx=5)
        task.bind("<Button-1>", self.start_drag)
        task.bind("<B1-Motion>", self.do_drag)
        task.bind("<ButtonRelease-1>", self.stop_drag)

        task_text_label = ctk.CTkLabel(
            task,
            text=f"{task_text} (Due: {due})",
            font=("Helvetica", 14),
            text_color="white",
            anchor="w",
            wraplength=400
        )
        task_text_label.pack(side=ctk.LEFT, expand=True, fill=ctk.X, padx=10, pady=5)

        check_btn = ctk.CTkButton(
            task,
            text="✔",
            command=lambda t=task: self.mark_done(t),
            font=("Helvetica", 14, "bold"),
            width=30,
            fg_color="white",
            text_color="#2ecc71",
            hover_color="#f0f0f0",
            corner_radius=8,
            height=30  # Consistent height
        )
        check_btn.pack(side=ctk.RIGHT, padx=10, pady=5)  # Adjusted padding

        self.tasks.append(task)
        self.task_entry.delete(0, ctk.END)

    def mark_done(self, task):
        def animate_tick(step=0):
            if step < 5:
                task.configure(fg_color="#2ecc71")
                task.after(100, lambda: animate_tick(step + 1))
            else:
                task.destroy()
                self.tasks.remove(task)

        animate_tick()

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Are you sure you want to remove all tasks?", parent=self):
            for task in self.tasks:
                task.destroy()
            self.tasks.clear()

    # Drag and Drop Handlers
    def start_drag(self, event):
        self.drag_data["widget"] = event.widget
        self.drag_data["y"] = event.y_root

    def do_drag(self, event):
        widget = self.drag_data["widget"]
        if widget:
            delta_y = event.y_root - self.drag_data["y"]
            index = self.tasks.index(widget)
            new_index = index

            if delta_y < -30 and index > 0:
                new_index = index - 1
            elif delta_y > 30 and index < len(self.tasks) - 1:
                new_index = index + 1

            if new_index != index:
                widget.pack_forget()
                self.tasks.pop(index)
                self.tasks.insert(new_index, widget)
                widget.pack(
                    in_=self.task_frame,
                    after=self.tasks[new_index - 1] if new_index > 0 else None,
                    before=self.tasks[new_index + 1] if new_index < len(self.tasks) - 1 else None
                )
                self.drag_data["y"] = event.y_root

    def stop_drag(self, event):
        self.drag_data = {"widget": None, "y": 0}

class MainScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EduLite OS - Main Dashboard")
        self.geometry("1000x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Load and set blurred background image for the entire app
        self.bg_image = Image.open("background.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1000, 600), Image.Resampling.LANCZOS)
        self.bg_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=5))  # Apply blur
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main Screen Layout
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=10, fg_color="#4285f4")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)

        self.sidebar_label = ctk.CTkLabel(
            self.sidebar,
            text="Dashboard",
            font=("Helvetica", 16, "bold"),
            text_color="white"
        )
        self.sidebar_label.pack(pady=20)

        # Add ToDo Widget to Main Screen
        self.todo_widget = ToDoWidget(self, width=650, height=550, corner_radius=10)
        self.todo_widget.pack(side=ctk.RIGHT, padx=10, pady=10, fill=ctk.BOTH, expand=True)

if __name__ == "__main__":
    app = MainScreen()
    app.mainloop()