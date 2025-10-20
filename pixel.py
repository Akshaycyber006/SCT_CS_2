from tkinter import Tk, Button, Label, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

class SimpleImageEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Encryptor")
        self.root.geometry("500x400")
        
        # Key for encryption (can be changed)
        self.key = 123  # Simple integer key
        
        # Create UI elements
        Label(root, text="Simple Image Encryption Tool", font=("Arial", 14)).pack(pady=10)
        
        self.original_label = Label(root, text="Original Image")
        self.original_label.pack(pady=5)
        
        self.encrypted_label = Label(root, text="Encrypted Image")
        self.encrypted_label.pack(pady=5)
        
        # Buttons
        Button(root, text="Load Image", command=self.load_image, width=15).pack(pady=5)
        Button(root, text="Encrypt Image", command=self.encrypt_image, width=15).pack(pady=5)
        Button(root, text="Decrypt Image", command=self.decrypt_image, width=15).pack(pady=5)
        Button(root, text="Save Result", command=self.save_image, width=15).pack(pady=5)
        
        # Image variables
        self.original_image = None
        self.encrypted_image = None
        self.display_original = None
        self.display_encrypted = None
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image, self.original_label)
                messagebox.showinfo("Success", "Image loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_image(self, image, label):
        # Resize for display
        image_copy = image.copy()
        image_copy.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image_copy)
        label.config(image=photo)
        label.image = photo  # Keep reference
    
    def encrypt_image(self):
        if not self.original_image:
            messagebox.showerror("Error", "Please load an image first")
            return
            
        try:
            # Convert to numpy array
            img_array = np.array(self.original_image)
            
            # Apply XOR encryption
            encrypted_array = img_array ^ self.key
            
            # Convert back to image
            self.encrypted_image = Image.fromarray(encrypted_array.astype(np.uint8))
            self.display_image(self.encrypted_image, self.encrypted_label)
            messagebox.showinfo("Success", "Image encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def decrypt_image(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "Please encrypt an image first")
            return
            
        try:
            # Convert to numpy array
            img_array = np.array(self.encrypted_image)
            
            # XOR is its own inverse - same operation decrypts
            decrypted_array = img_array ^ self.key
            
            # Convert back to image
            decrypted_image = Image.fromarray(decrypted_array.astype(np.uint8))
            self.display_image(decrypted_image, self.encrypted_label)
            messagebox.showinfo("Success", "Image decrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
    
    def save_image(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "No image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
        )
        
        if file_path:
            try:
                self.encrypted_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# Create and run the application
if __name__ == "__main__":
    root = Tk()
    app = SimpleImageEncryptor(root)
    root.mainloop()