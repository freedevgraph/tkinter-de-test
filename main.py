import tkinter as tk
from tkinter import messagebox
import time

class VirtualDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter OS - Virtual Desktop")
        self.root.geometry("1024x768")
        self.root.configure(bg="#2c3e50")
        
        # Track window instances
        self.window_count = 0
        
        # Initialize UI Components
        self.create_workspace()
        self.create_taskbar()
        self.create_start_menu()
        
    def create_workspace(self):
        """Creates the main area where app windows live."""
        self.workspace = tk.Canvas(self.root, bg="#34495e", highlightthickness=0)
        self.workspace.pack(fill=tk.BOTH, expand=True)
        
        # Desktop Shortcut Example
        self.create_desktop_icon("Text Editor", 40, 40, self.open_text_editor)
        self.create_desktop_icon("Calculator", 40, 140, self.open_calculator)

    def create_desktop_icon(self, label_text, x, y, command):
        """Generates clickable shortcut icons on the canvas."""
        btn = tk.Button(self.workspace, text="📁\n" + label_text, font=("Arial", 10),
                        bg="#34495e", fg="white", bd=0, activebackground="#1abc9c",
                        activeforeground="white", cursor="hand2", command=command)
        self.workspace.create_window(x, y, window=btn, anchor="nw")

    def create_taskbar(self):
        """Creates the bottom bar containing system utilities."""
        self.taskbar = tk.Frame(self.root, bg="#2c3e50", height=40)
        self.taskbar.pack(fill=tk.X, side=tk.BOTTOM)
        self.taskbar.pack_propagate(False)
        
        # Start Button
        self.start_btn = tk.Button(self.taskbar, text="❖ Start", font=("Arial", 11, "bold"),
                                   bg="#e74c3c", fg="white", bd=0, padx=15, 
                                   activebackground="#c0392b", command=self.toggle_start_menu)
        self.start_btn.pack(side=tk.LEFT, fill=tk.Y)
        
        # Clock / System Time
        self.clock_label = tk.Label(self.taskbar, text="", font=("Arial", 11), bg="#2c3e50", fg="white", padx=15)
        self.clock_label.pack(side=tk.RIGHT, fill=tk.Y)
        self.update_clock()

    def update_clock(self):
        """Maintains the background thread updating taskbar time."""
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def create_start_menu(self):
        """Builds the popup application drawer."""
        self.start_menu = tk.Frame(self.root, bg="#1a252f", bd=2, relief=tk.RAISED)
        
        # Start Menu App Links
        apps = [
            ("Text Editor", self.open_text_editor),
            ("Calculator", self.open_calculator),
            ("Terminal Simulation", self.open_terminal),
            ("Shutdown", self.root.quit)
        ]
        
        for name, cmd in apps:
            btn = tk.Button(self.start_menu, text=name, font=("Arial", 11), anchor="w",
                            bg="#1a252f", fg="white", bd=0, padx=20, pady=8,
                            activebackground="#34495e", activeforeground="white", command=cmd)
            btn.pack(fill=tk.X)

    def toggle_start_menu(self):
        """Handles closing and opening logic for the panel."""
        if self.start_menu.winfo_viewable():
            self.start_menu.place_forget()
        else:
            # Place right above the bottom taskbar
            self.start_menu.place(x=0, y=self.root.winfo_height() - 200, width=220, height=160)
            self.start_menu.lift()

    def create_window(self, title, width, height):
        """Generates a custom draggable floating sub-window container."""
        self.start_menu.place_forget() # Close menu on action
        self.window_count += 1
        
        # Coordinates offset per spawn
        offset = (self.window_count % 5) * 30
        x, y = 150 + offset, 100 + offset
        
        # Base window Frame
        win_frame = tk.Frame(self.workspace, bg="#ecf0f1", bd=2, relief=tk.RAISED)
        
        # Title bar custom styling
        title_bar = tk.Frame(win_frame, bg="#2980b9", height=30)
        title_bar.pack(fill=tk.X, side=tk.TOP)
        title_bar.pack_propagate(False)
        
        title_lbl = tk.Label(title_bar, text=title, bg="#2980b9", fg="white", font=("Arial", 10, "bold"), pl=5)
        title_lbl.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(title_bar, text=" ✕ ", bg="#e74c3c", fg="white", bd=0, 
                             activebackground="#c0392b", command=win_frame.destroy)
        close_btn.pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        
        # Window Content App canvas container
        content_area = tk.Frame(win_frame, bg="#ecf0f1")
        content_area.pack(fill=tk.BOTH, expand=True)
        
        # Render onto workspace
        self.workspace.create_window(x, y, window=win_frame, width=width, height=height, anchor="nw", tags=f"win_{id(win_frame)}")
        
        # Window Dragging Functionality
        def start_drag(event):
            win_frame.startX = event.x
            win_frame.startY = event.y

        def drag(event):
            # Track difference against root container coordinates
            deltax = event.x - win_frame.startX
            deltay = event.y - win_frame.startY
            new_x = win_frame.winfo_x() + deltax
            new_y = win_frame.winfo_y() + deltay
            self.workspace.moveto(f"win_{id(win_frame)}", new_x, new_y)

        title_bar.bind("<Button-1>", start_drag)
        title_bar.bind("<B1-Motion>", drag)
        title_lbl.bind("<Button-1>", start_drag)
        title_lbl.bind("<B1-Motion>", drag)
        
        return content_area

    # --- NATIVE APPLICATION CODE SPECIFICS ---
    
    def open_text_editor(self):
        container = self.create_window("Text Editor", 400, 300)
        txt = tk.Text(container, font=("Courier", 10), bd=0)
        txt.pack(fill=tk.BOTH, expand=True)

    def open_calculator(self):
        container = self.create_window("Calc", 250, 320)
        expr_var = tk.StringVar()
        
        entry = tk.Entry(container, textvariable=expr_var, font=("Arial", 16), justify="right", bd=5)
        entry.pack(fill=tk.X, padx=5, pady=5)
        
        grid_frame = tk.Frame(container, bg="#ecf0f1")
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        def calc_press(key):
            if key == '=':
                try: expr_var.set(eval(expr_var.get()))
                except: expr_var.set("Error")
            elif key == 'C': expr_var.set("")
            else: expr_var.set(expr_var.get() + key)

        r, c = 0, 0
        for btn_text in buttons:
            b = tk.Button(grid_frame, text=btn_text, font=("Arial", 12), bd=1,
                          command=lambda x=btn_text: calc_press(x))
            b.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
            c += 1
            if c > 3: c = 0; r += 1
            
        for i in range(4):
            grid_frame.rowconfigure(i, weight=1)
            grid_frame.columnconfigure(i, weight=1)

    def open_terminal(self):
        container = self.create_window("System Terminal", 450, 250)
        term_text = tk.Text(container, bg="black", fg="#00ff00", font=("Courier", 10), insertbackground="white")
        term_text.pack(fill=tk.BOTH, expand=True)
        term_text.insert(tk.END, "TkinterOS kernel v1.0.0 initialized.\nType 'help' for commands.\n\n$ ")
        
        def process_cmd(event):
            # Extract current line string text
            lines = term_text.get("1.0", tk.END).strip().split('\n')
            last_line = lines[-1].replace("$ ", "").strip()
            
            if last_line == "help":
                output = "\nAvailable Commands:\n - help: Show list\n - clear: Wipe screen\n - hello: Greet user\n"
            elif last_line == "clear":
                term_text.delete("1.0", tk.END)
                term_text.insert(tk.END, "$ ")
                return "break"
            elif last_line == "hello":
                output = "\nHello from the Tkinter virtual space!\n"
            elif last_line == "":
                output = ""
            else:
                output = f"\nCommand not found: '{last_line}'\n"
                
            term_text.insert(tk.END, output + "\n$ ")
            term_text.see(tk.END)
            return "break" # Overrides standard newline action execution
            
        term_text.bind("<Return>", process_cmd)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualDesktop(root)
    root.mainloop()
