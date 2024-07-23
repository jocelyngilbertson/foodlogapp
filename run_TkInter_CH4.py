import subprocess
import sys
import csv 
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import cv2
import requests
import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api_keys import EDAMAM_APP_ID, EDAMAM_APP_KEY

class MealTrackerApp:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.root.title("Meal Tracker App")

        # Connect to the database
        self.conn = sqlite3.connect('meal_tracker.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Setup frames
        self.setup_frames()

        # Setup widgets
        self.setup_widgets()

        self.food_items = []
        self.cap = None
        self.previewing = False

        # Load existing entries from the database
        self.load_entries()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS food_log (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                barcode TEXT,
                                food_name TEXT,
                                servings REAL
                              )''')
        self.conn.commit()

    def setup_frames(self):
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(pady=10)

        self.middle_frame = ttk.Frame(self.root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(pady=10)

        self.camera_frame = ttk.Frame(self.root)
        self.camera_frame.pack(pady=10)
        
        
    def export_all_to_file(self):
        with open('meal_tracker_export.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Barcode", "Food Name", "Servings (g)"])  # header row
            for item in self.food_items:
                writer.writerow([item['barcode'], item['food_name'], item['servings']])

        messagebox.showinfo("Export Successful", "All meal entries have been exported to meal_tracker_export.csv")

    def setup_widgets(self):
        # Barcode Entry
        ttk.Label(self.top_frame, text="Barcode:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.barcode_entry = ttk.Entry(self.top_frame, width=50)
        self.barcode_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Scan Barcode Button
        self.scan_button = ttk.Button(self.top_frame, text="Scan Barcode", command=self.toggle_preview, bootstyle=PRIMARY)
        self.scan_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        # Look Up Button
        self.lookup_button = ttk.Button(self.top_frame, text="Look Up Barcode", command=self.lookup_food_manual, bootstyle=SUCCESS)
        self.lookup_button.grid(row=2, column=2, padx=5, pady=5, sticky='ew')

        # Food Name Entry
        ttk.Label(self.top_frame, text="Food Name:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.food_name_entry = ttk.Entry(self.top_frame, width=50)
        self.food_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.food_name_entry.bind('<KeyRelease>', self.autocomplete_food_name)

        # Auto-complete Listbox
        ttk.Label(self.top_frame, text="List of Foods:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.autocomplete_listbox = tk.Listbox(self.top_frame, width=50)
        self.autocomplete_listbox.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.autocomplete_listbox.bind("<<ListboxSelect>>", self.on_autocomplete_select)

        # Servings Entry
        ttk.Label(self.top_frame, text="Servings (grams):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.servings_entry = ttk.Entry(self.top_frame, width=50)
        self.servings_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        # Log Food Button
        self.log_button = ttk.Button(self.top_frame, text="Log Food", command=self.log_food, bootstyle=PRIMARY)
        self.log_button.grid(row=4, column=2, padx=5, pady=5, sticky='ew')

        # a bit of space
        horizontal_spacer = ttk.Frame(self.top_frame, height=20)
        horizontal_spacer.grid(row=5, column=0, columnspan=2)

        # Listbox for logged food items
        self.food_listbox = tk.Listbox(self.top_frame, width=70, height=10)
        self.food_listbox.grid(row=6, column=1, padx=5, sticky='ew')

        # Scrollbar for listbox
        self.scrollbar = ttk.Scrollbar(self.top_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.food_listbox.yview)
        self.scrollbar.grid(row=6, column=2, sticky='wns')

        self.food_listbox.config(yscrollcommand=self.scrollbar.set)

        # frame for remove and export buttons in column 0
        self.button_frame = ttk.Frame(self.top_frame)
        self.button_frame.grid(row=7, column=1, pady=5, sticky='ew')

        
        # Remove Item Button
        self.remove_button = ttk.Button(self.button_frame, text="Remove Selected Item", command=self.remove_item, bootstyle=DANGER)
        self.remove_button.grid(row=0, column=0, padx=5)

        # Export All to File Button
        self.export_button = ttk.Button(self.button_frame, text="Export All to File", command=self.export_all_to_file, bootstyle=SUCCESS)
        self.export_button.grid(row=0, column=1, padx=5)
        
        # Camera Preview Label
        self.camera_label = ttk.Label(self.top_frame)
        self.camera_label.grid(row=8, column=1, pady=5, sticky='nsew')



    def enable_lookup_button(self, event):
        if self.barcode_entry.get():
            self.lookup_button.config(state=tk.NORMAL)
        else:
            self.lookup_button.config(state=tk.DISABLED)
    def toggle_preview(self):
        if self.previewing:
            self.previewing = False
            self.cap.release()
            self.camera_label.config(image='')
        else:
            self.previewing = True
            self.cap = cv2.VideoCapture(0)
            self.preview_camera()
        self.barcode_entry.delete(0, tk.END)

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
        
        if response.status_code == 200:
            data = response.json()
            if 'parsed' in data and data['parsed']:
                food = data['parsed'][0]['food']
            elif 'hints' in data and data['hints']:
                food = data['hints'][0]['food']
            else:
                messagebox.showerror("API Error", "Unable to fetch nutritional data.")
                return
            
            food_label = food['label']
            servings = self.get_serving_in_grams(food)
            if servings is None:
                servings = 1

            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, food_label)
            self.servings_entry.delete(0, tk.END)
            self.servings_entry.insert(0, servings)
        elif response.status_code == 404:
            messagebox.showerror("API Error", "Barcode not found. Please manually enter your item in 'food name.'")
        else:
            messagebox.showerror("API Error", f"An error occurred: {response.status_code}")

    def lookup_food_manual(self):
        barcode = self.barcode_entry.get()
        if barcode:
            self.lookup_food(barcode)
        else:
            messagebox.showerror("Input Error", "Please enter a barcode to look up.")

    def autocomplete_food_name(self, event):
        query = self.food_name_entry.get()
        if not query:
            self.autocomplete_listbox.delete(0, tk.END)
            return
        if len(query) < 3: # Don't search until at least 3 characters are entered
            return
            

        url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={query}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            self.autocomplete_listbox.delete(0, tk.END)
            if 'hints' in data and data['hints']:
                    for item in data['hints']:
                        food= item['food']
                        food_label = food['label']
                        food_brand = food.get('brand',"")
                        food_category = food.get('category',"")
                        text = f"{food_label}, {food_brand}"
                        self.autocomplete_listbox.insert(tk.END, text)
                        self.autocomplete_listbox.see(tk.END)
                        self.autocomplete_listbox.update()
        else:
            self.autocomplete_listbox.delete(0, tk.END)

    def on_autocomplete_select(self, event):
        selection = self.autocomplete_listbox.curselection()
        if selection:
            index = selection[0]
            food_name = self.autocomplete_listbox.get(index)
            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, food_name)
            self.autocomplete_listbox.delete(0, tk.END)

            # Fetch servings information based on the selected food name
            self.fetch_servings(food_name)

    def fetch_servings(self, food_name):
        url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={food_name}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'parsed' in data and data['parsed']:
                food = data['parsed'][0]['food']
            elif 'hints' in data and data['hints']:
                food = data['hints'][0]['food']
            else:
                messagebox.showerror("API Error", "Unable to fetch nutritional data.")
                return
            
            servings = self.get_serving_in_grams(food)
            if servings is None:
                servings = 1

            self.servings_entry.delete(0, tk.END)
            self.servings_entry.insert(0, servings)
        else:
            messagebox.showerror("API Error", f"An error occurred: {response.status_code}")

    def get_serving_in_grams(self, food):
        serving_size = None
        if 'servingSizes' in food and food['servingSizes']:
            for serving in food['servingSizes']:
                if serving['label'].lower() == 'gram':
                    serving_size = serving['quantity']
                    break
        return serving_size

    def log_food(self):
        barcode = self.barcode_entry.get()
        food_name = self.food_name_entry.get()
        servings = self.servings_entry.get()

        if not food_name or not servings:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            servings = float(servings)
        except ValueError:
            messagebox.showerror("Input Error", "Servings must be a number.")
            return

        self.food_items.append({
            'barcode': barcode,
            'food_name': food_name,
            'servings': servings
        })
        self.food_listbox.insert(tk.END, f"{food_name} - {servings}g")

        # Insert the entry into the database
        self.cursor.execute('INSERT INTO food_log (barcode, food_name, servings) VALUES (?, ?, ?)',
                            (barcode, food_name, servings))
        self.conn.commit()

        # Clear the input fields
        self.barcode_entry.delete(0, tk.END)
        self.food_name_entry.delete(0, tk.END)
        self.servings_entry.delete(0, tk.END)

    def load_entries(self):
        self.cursor.execute('SELECT id, barcode, food_name, servings FROM food_log')
        rows = self.cursor.fetchall()
        for row in rows:
            food_id, barcode, food_name, servings = row
            self.food_items.append({
                'id': food_id,
                'barcode': barcode,
                'food_name': food_name,
                'servings': servings
            })
            self.food_listbox.insert(tk.END, f"{food_name} - {servings}g")

    def remove_item(self):
        selected = self.food_listbox.curselection()
        if selected:
            index = selected[0]
            food_item = self.food_items.pop(index)
            self.food_listbox.delete(index)

            # Delete the entry from the database
            self.cursor.execute('DELETE FROM food_log WHERE id = ?', (food_item['id'],))
            self.conn.commit()

    def __del__(self):
        if self.cap:
            self.cap.release()
        self.conn.close()

if __name__ == "__main__":
    root = ttk.Window(themename="journal")
    app = MealTrackerApp(root)
    root.mainloop()
