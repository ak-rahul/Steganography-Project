"""Encryption tab GUI - Standard Tkinter"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
from pathlib import Path

from core.steganography import Steganography
from core.encryption import PasswordEncryption
from config import SUPPORTED_FORMATS, MAX_IMAGE_SIZE, MIN_PASSWORD_LENGTH, OUTPUT_DIR


class EncryptTab(tk.Frame):
    """Encryption interface"""
    
    def __init__(self, parent, bg_color, fg_color):
        super().__init__(parent, bg=bg_color)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.selected_image = None
        self.image_label_widget = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create encryption tab widgets"""
        
        # Left panel - Image selection
        left_frame = tk.Frame(self, bg="#313244")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        tk.Label(
            left_frame,
            text="Select Cover Image",
            bg="#313244",
            fg=self.fg_color,
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Image display frame
        self.image_frame = tk.Frame(left_frame, bg="#1e1e2e", width=400, height=400, relief=tk.SOLID, bd=1)
        self.image_frame.pack(pady=10, padx=10)
        self.image_frame.pack_propagate(False)
        
        # Placeholder
        tk.Label(
            self.image_frame,
            text="📷\n\nNo image selected",
            bg="#1e1e2e",
            fg="#6c7086",
            font=('Segoe UI', 12)
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Select image button
        tk.Button(
            left_frame,
            text="📁 Browse Image",
            command=self.select_image,
            bg="#89b4fa",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#74c7ec",
            activeforeground="#000000"
        ).pack(pady=10)
        
        # Image info label
        self.info_label = tk.Label(
            left_frame,
            text="",
            bg="#313244",
            fg="#a6adc8",
            font=('Segoe UI', 9),
            wraplength=400
        )
        self.info_label.pack(pady=5)
        
        # Right panel - Message input
        right_frame = tk.Frame(self, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        tk.Label(
            right_frame,
            text="🔐 Enter Secret Message",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Password section
        pwd_frame = tk.Frame(right_frame, bg=self.bg_color)
        pwd_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(
            pwd_frame,
            text="Password:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            pwd_frame,
            show="●",
            font=('Segoe UI', 11),
            bg="#313244",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=0
        )
        self.password_entry.pack(fill=tk.X, pady=5, ipady=8)
        
        # Show password checkbox
        self.show_pwd_var = tk.BooleanVar()
        tk.Checkbutton(
            pwd_frame,
            text="Show password",
            variable=self.show_pwd_var,
            command=self.toggle_password,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor="#313244",
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
            font=('Segoe UI', 9)
        ).pack(anchor=tk.W, pady=2)
        
        # Message section
        msg_frame = tk.Frame(right_frame, bg=self.bg_color)
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        tk.Label(
            msg_frame,
            text="Secret Message:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor=tk.W)
        
        # Text widget with scrollbar
        self.message_text = scrolledtext.ScrolledText(
            msg_frame,
            font=('Segoe UI', 10),
            wrap=tk.WORD,
            height=15,
            bg="#313244",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=0
        )
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Character counter
        self.char_label = tk.Label(
            msg_frame,
            text="Characters: 0",
            bg=self.bg_color,
            fg="#6c7086",
            font=('Segoe UI', 9)
        )
        self.char_label.pack(anchor=tk.E, pady=5)
        
        self.message_text.bind('<KeyRelease>', self.update_char_count)
        
        # Action buttons
        btn_frame = tk.Frame(right_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Button(
            btn_frame,
            text="✓ Encrypt & Save",
            command=self.encrypt_message,
            bg="#a6e3a1",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#94e2d5",
            activeforeground="#000000"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✕ Clear All",
            command=self.clear_fields,
            bg="#f38ba8",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#eba0ac",
            activeforeground="#000000"
        ).pack(side=tk.RIGHT, padx=5)
    
    def select_image(self):
        """Open file dialog to select image"""
        filename = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=SUPPORTED_FORMATS
        )
        
        if filename:
            self.selected_image = filename
            self.display_image(filename)
            self.show_image_info(filename)
    
    def display_image(self, image_path):
        """Display selected image"""
        try:
            # Clear previous image
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            
            # Load and resize image
            img = Image.open(image_path)
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Display image
            self.image_label_widget = tk.Label(self.image_frame, image=photo, bg="#1e1e2e")
            self.image_label_widget.image = photo  # Keep reference
            self.image_label_widget.pack(expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def show_image_info(self, image_path):
        """Show image capacity information"""
        result = Steganography.get_image_capacity(image_path)
        if result['success']:
            self.info_label.config(
                text=f"✓ Image loaded successfully\n"
                     f"Capacity: {result['max_characters']} characters | "
                     f"Dimensions: {result['image_dimensions']}"
            )
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_pwd_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def update_char_count(self, event=None):
        """Update character counter"""
        count = len(self.message_text.get("1.0", "end-1c"))
        self.char_label.config(text=f"Characters: {count}")
    
    def encrypt_message(self):
        """Encrypt and embed message"""
        # Validate inputs
        if not self.selected_image:
            messagebox.showwarning("No Image", "Please select a cover image first!")
            return
        
        password = self.password_entry.get()
        if len(password) < MIN_PASSWORD_LENGTH:
            messagebox.showwarning(
                "Weak Password",
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters long!"
            )
            return
        
        message = self.message_text.get("1.0", "end-1c").strip()
        if not message:
            messagebox.showwarning("No Message", "Please enter a message to hide!")
            return
        
        try:
            # Encrypt message
            encrypted_msg = PasswordEncryption.encrypt_message(message, password)
            
            # Generate output filename
            base_name = Path(self.selected_image).stem
            output_path = os.path.join(
                OUTPUT_DIR,
                f"{base_name}_encrypted_{len(os.listdir(OUTPUT_DIR))}.png"
            )
            
            # Encode into image
            result = Steganography.encode_message(
                self.selected_image,
                encrypted_msg,
                output_path
            )
            
            if result['success']:
                messagebox.showinfo(
                    "✓ Success",
                    f"Message encrypted successfully!\n\n"
                    f"📁 Saved to: {output_path}\n"
                    f"📝 Message length: {len(message)} characters\n"
                    f"📊 Capacity used: {result['capacity_used']:.2f}%"
                )
                self.clear_fields()
            else:
                messagebox.showerror("Error", result['error'])
                
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))
    
    def clear_fields(self):
        """Clear all input fields"""
        self.selected_image = None
        self.password_entry.delete(0, tk.END)
        self.message_text.delete("1.0", tk.END)
        self.char_label.config(text="Characters: 0")
        
        # Reset image frame
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        tk.Label(
            self.image_frame,
            text="📷\n\nNo image selected",
            bg="#1e1e2e",
            fg="#6c7086",
            font=('Segoe UI', 12)
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.info_label.config(text="")
