"""Main application window - Standard Tkinter version"""

import tkinter as tk
from tkinter import ttk
from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from gui.encrypt_tab import EncryptTab
from gui.decrypt_tab import DecryptTab


class MainWindow:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Dark theme colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        
        self.root.configure(bg=self.bg_color)
        
        # Center window
        self.position_center()
        
        # Create UI
        self.create_widgets()
    
    def position_center(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = WINDOW_WIDTH
        height = WINDOW_HEIGHT
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create main window widgets"""
        
        # Header frame
        header_frame = tk.Frame(self.root, bg="#313244", height=100)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=APP_NAME,
            font=('Segoe UI', 24, 'bold'),
            bg="#313244",
            fg=self.fg_color
        ).pack(pady=15)
        
        tk.Label(
            header_frame,
            text="Hide and reveal secret messages in images using steganography",
            font=('Segoe UI', 10),
            bg="#313244",
            fg="#a6adc8"
        ).pack()
        
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure tab colors
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#313244', 
                       foreground=self.fg_color,
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.accent_color)],
                 foreground=[('selected', '#000000')])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.encrypt_tab = EncryptTab(self.notebook, self.bg_color, self.fg_color)
        self.decrypt_tab = DecryptTab(self.notebook, self.bg_color, self.fg_color)
        
        self.notebook.add(self.encrypt_tab, text="  Encrypt Message  ")
        self.notebook.add(self.decrypt_tab, text="  Decrypt Message  ")
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#313244", height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            footer_frame,
            text=f"Version {APP_VERSION} | LSB Steganography with AES Encryption",
            font=('Segoe UI', 8),
            bg="#313244",
            fg="#6c7086"
        ).pack(pady=5)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
