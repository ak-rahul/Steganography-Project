"""Decryption tab GUI - Standard Tkinter"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

from core.steganography import Steganography
from core.encryption import PasswordEncryption
from config import SUPPORTED_FORMATS, MAX_IMAGE_SIZE, OUTPUT_DIR


class DecryptTab(tk.Frame):
    """Decryption interface"""
    
    def __init__(self, parent, bg_color, fg_color):
        super().__init__(parent, bg=bg_color)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.selected_image = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create decryption tab widgets"""
        
        # Left panel
        left_frame = tk.Frame(self, bg="#313244")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        tk.Label(
            left_frame,
            text="Select Encrypted Image",
            bg="#313244",
            fg=self.fg_color,
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Image display
        self.image_frame = tk.Frame(left_frame, bg="#1e1e2e", width=400, height=400, relief=tk.SOLID, bd=1)
        self.image_frame.pack(pady=10, padx=10)
        self.image_frame.pack_propagate(False)
        
        tk.Label(
            self.image_frame,
            text="🔒\n\nNo encrypted image selected",
            bg="#1e1e2e",
            fg="#6c7086",
            font=('Segoe UI', 12)
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Select button
        tk.Button(
            left_frame,
            text="📁 Browse Encrypted Image",
            command=self.select_image,
            bg="#f9e2af",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#f5c2e7",
            activeforeground="#000000"
        ).pack(pady=10)
        
        # Right panel
        right_frame = tk.Frame(self, bg=self.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            right_frame,
            text="🔓 Decrypt Secret Message",
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Password section
        pwd_frame = tk.Frame(right_frame, bg=self.bg_color)
        pwd_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(
            pwd_frame,
            text="Enter Password:",
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
        
        # Show password
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
        
        # Decrypt button
        tk.Button(
            pwd_frame,
            text="🔓 Decrypt Message",
            command=self.decrypt_message,
            bg="#a6e3a1",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#94e2d5",
            activeforeground="#000000"
        ).pack(pady=15)
        
        # Message display
        msg_frame = tk.Frame(right_frame, bg=self.bg_color)
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        tk.Label(
            msg_frame,
            text="Decrypted Message:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor=tk.W)
        
        # Text display with scrollbar
        self.message_text = scrolledtext.ScrolledText(
            msg_frame,
            font=('Segoe UI', 10),
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED,
            bg="#313244",
            fg=self.fg_color,
            relief=tk.FLAT,
            bd=0
        )
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Action buttons
        btn_frame = tk.Frame(right_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Button(
            btn_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_message,
            bg="#89b4fa",
            fg="#000000",
            font=('Segoe UI', 10, 'bold'),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            activebackground="#74c7ec",
            activeforeground="#000000"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="✕ Clear",
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
        """Select encrypted image"""
        filename = filedialog.askopenfilename(
            title="Select Encrypted Image",
            filetypes=SUPPORTED_FORMATS,
            initialdir=OUTPUT_DIR
        )
        
        if filename:
            self.selected_image = filename
            self.display_image(filename)
    
    def display_image(self, image_path):
        """Display encrypted image"""
        try:
            for widget in self.image_frame.winfo_children():
                widget.destroy()
            
            img = Image.open(image_path)
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            label = tk.Label(self.image_frame, image=photo, bg="#1e1e2e")
            label.image = photo
            label.pack(expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_pwd_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def decrypt_message(self):
        """Decrypt message from image"""
        if not self.selected_image:
            messagebox.showwarning("No Image", "Please select an encrypted image first!")
            return
        
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("No Password", "Please enter the password!")
            return
        
        try:
            # Extract encrypted message
            result = Steganography.decode_message(self.selected_image)
            
            if not result['success']:
                messagebox.showerror("Error", result['error'])
                return
            
            encrypted_msg = result['message']
            
            # Decrypt message
            try:
                decrypted_msg = PasswordEncryption.decrypt_message(
                    encrypted_msg,
                    password
                )
                
                # Display decrypted message
                self.message_text.config(state=tk.NORMAL)
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", decrypted_msg)
                self.message_text.config(state=tk.DISABLED)
                
                messagebox.showinfo(
                    "✓ Success",
                    f"Message decrypted successfully!\n"
                    f"📝 Length: {len(decrypted_msg)} characters"
                )
                
            except ValueError as e:
                messagebox.showerror("❌ Decryption Failed", 
                                   "Incorrect password or corrupted data!")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def copy_message(self):
        """Copy decrypted message to clipboard"""
        message = self.message_text.get("1.0", "end-1c")
        if message.strip():
            self.clipboard_clear()
            self.clipboard_append(message)
            messagebox.showinfo("✓ Copied", "Message copied to clipboard!")
        else:
            messagebox.showwarning("No Message", "No message to copy!")
    
    def clear_fields(self):
        """Clear all fields"""
        self.selected_image = None
        self.password_entry.delete(0, tk.END)
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete("1.0", tk.END)
        self.message_text.config(state=tk.DISABLED)
        
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        tk.Label(
            self.image_frame,
            text="🔒\n\nNo encrypted image selected",
            bg="#1e1e2e",
            fg="#6c7086",
            font=('Segoe UI', 12)
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
