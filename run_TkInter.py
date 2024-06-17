import subprocess
import pkg_resources
import sys


def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def is_package_installed(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False
        
for pkg in ["requests", "pyzbar", "opencv-python"]:
    if not is_package_installed(pkg):
        print(f"Package {pkg} not found. Installing...")
        install_package(pkg)
 
# Install packages
install("opencv-python")
install("pyzbar")
install("requests")
 
# Note: 'tkinter' usually doesn't need to be installed via pip

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import pyzbar
import requests

# Replace with your Edamam API credentials
EDAMAM_APP_ID = 'your_app_id'
EDAMAM_APP_KEY = 'your_app_key'

class MealTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Tracker App")

        # Setup frames
        self.setup_frames()

        # Setup widgets
        self.setup_widgets()

        self.food_items = []
        self.cap = None
        self.previewing = False

    def setup_frames(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10)

        self.camera_frame = tk.Frame(self.root)
        self.camera_frame.pack(pady=10)

    def setup_widgets(self):
        # Barcode Entry
        tk.Label(self.top_frame, text="Barcode:").grid(row=0, column=0, padx=5, pady=5)
        self.barcode_entry = tk.Entry(self.top_frame, width=50)
        self.barcode_entry.grid(row=0, column=1, padx=5, pady=5)

        # Scan Barcode Button
        self.scan_button = tk.Button(self.top_frame, text="Scan Barcode", command=self.toggle_preview)
        self.scan_button.grid(row=0, column=2, padx=5, pady=5)

        # Food Name Entry
        tk.Label(self.top_frame, text="Food Name:").grid(row=1, column=0, padx=5, pady=5)
        self.food_name_entry = tk.Entry(self.top_frame, width=50)
        self.food_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Servings Entry
        tk.Label(self.top_frame, text="Servings (grams):").grid(row=2, column=0, padx=5, pady=5)
        self.servings_entry = tk.Entry(self.top_frame, width=50)
        self.servings_entry.grid(row=2, column=1, padx=5, pady=5)

        # Log Food Button
        self.log_button = tk.Button(self.middle_frame, text="Log Food", command=self.log_food)
        self.log_button.pack(pady=5)

        # Listbox for logged food items
        self.food_listbox = tk.Listbox(self.bottom_frame, width=80, height=10)
        self.food_listbox.pack(side=tk.LEFT, padx=5)

        # Scrollbar for listbox
        self.scrollbar = tk.Scrollbar(self.bottom_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.food_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.food_listbox.config(yscrollcommand=self.scrollbar.set)

        # Remove Item Button
        self.remove_button = tk.Button(self.bottom_frame, text="Remove Selected Item", command=self.remove_item)
        self.remove_button.pack(pady=5)

        # Camera Preview Label
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack(pady=10)

    def toggle_preview(self):
        if self.previewing:
            self.previewing = False
            self.cap.release()
            self.camera_label.config(image='')
        else:
            self.previewing = True
            self.cap = cv2.VideoCapture(0)
            self.preview_camera()

    def preview_camera(self):
        if self.previewing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.config(image=imgtk)

                # Detect barcodes in the frame
                for barcode in decode(frame):
                    barcode_data = barcode.data.decode('utf-8')
                    self.barcode_entry.delete(0, tk.END)
                    self.barcode_entry.insert(0, barcode_data)
                    self.lookup_food(barcode_data)
                    self.toggle_preview()  # Stop preview after scanning
                    return

            self.camera_label.after(10, self.preview_camera)

    def lookup_food(self, barcode):
        url = f"https://api.edamam.com/api/food-database/v2/parser?upc={barcode}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        response = requests.get(url)
        data = response.json()
        if 'parsed' in data and data['parsed']:
            food = data['parsed'][0]['food']
            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, food['label'])
        else:
            messagebox.showerror("API Error", "Unable to fetch nutritional data.")

    def log_food(self):
        barcode = self.barcode_entry.get()
        food_name = self.food_name_entry.get()
        servings = self.servings_entry.get()

        if not food_name or not servings:
            messagebox.showerror("Input Error", "Please provide both food name and servings.")
            return

        try:
            servings = float(servings)
        except ValueError:
            messagebox.showerror("Input Error", "Servings must be a number.")
            return

        nutritional_data = {
            'food_name': food_name,
            'servings': servings
        }

        self.food_items.append(nutritional_data)
        self.food_listbox.insert(tk.END, f"{nutritional_data['food_name']} - {nutritional_data['servings']}g")

    def remove_item(self):
        selected = self.food_listbox.curselection()
        if selected:
            self.food_listbox.delete(selected[0])
            del self.food_items[selected[0]]

if __name__ == "__main__":
    root = tk.Tk()
    app = MealTrackerApp(root)
    root.mainloop()
