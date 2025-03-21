import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json
import pyautogui

class CalibrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calibration Tool")
        self.root.geometry("300x300")
        self.root.attributes("-topmost", True)  # Make window always stay on top

        with open("scripts/locations.json", "r") as f:
            locations = json.load(f)

        # List of categories for the dropdown menu
        self.categories = list(locations.keys())

        # Create a label for the dropdown menu
        self.dropdown_label = tk.Label(root, text="Select an option:")
        self.dropdown_label.pack()

        # Create the dropdown menu
        self.selected_category = tk.StringVar(root)
        self.selected_category.set(self.categories[0])  # Set default option
        self.dropdown_menu = tk.OptionMenu(root, self.selected_category, *self.categories)
        self.dropdown_menu.pack()

        self.output_text = ScrolledText(root, wrap=tk.WORD, height=3, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.key_label = tk.Label(root, text="Enter key for position:")
        self.key_label.pack()

        self.key_entry = tk.Entry(root)
        self.key_entry.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_capture_mode)
        self.reset_button.pack(pady=5)

        self.capture_mode = True  # Flag to toggle between modes
        self.record_mode = False
        self.show_start_text()

        self.selected_category.trace('w', self.display_location_keys)

        self.root.bind('<Return>', self.on_enter)  # Bind Enter key to on_enter method

    def show_start_text(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Select a category above.\n")
        self.output_text.insert(tk.END, f"Then type a key below to update.\n")
        self.output_text.config(state=tk.DISABLED)

    def reset_capture_mode(self):
        self.capture_mode = True
        self.show_start_text()

    def display_location_keys(self, *args):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        with open("scripts/locations.json", "r") as f:
            locations = json.load(f)
        self.output_text.insert(tk.END, f"Keys for '{self.selected_category.get()}':\n")
        for key in locations[self.selected_category.get()].keys():
            self.output_text.insert(tk.END, f"{key}: {locations[self.selected_category.get()][key]['coordinates']}\n")
        self.output_text.config(state=tk.DISABLED)

    def on_enter(self, event):
        with open("scripts/locations.json", "r") as f:
            locations = json.load(f)
        key = self.key_entry.get()
        category = self.selected_category.get()
        if self.capture_mode:
            if not key:
                self.status_label.config(text="Please enter a key before confirming.")
                return
            if key not in locations[category]:
                if self.record_mode: # add new variable
                    self.status_label.config(text=f"'{key}' recorded.")
                    self.status_label.config(text=f"Location: '{key}'confirmed.\nPress Enter to capture mouse position.")
                    self.capture_mode = False
                    self.record_mode = False
                else:
                    self.status_label.config(text=f"'{key}' not in '{category}'")
                    self.status_label.config(text=f"Press enter again to record '{key}' as a new key.")
                    self.record_mode = True
            else:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"{key}\n{locations[self.selected_category.get()][key]['description']}\n\nPress Reset below to remove selection")
                self.output_text.config(state=tk.DISABLED)
                self.status_label.config(text=f"Location: '{key}'confirmed.\nPress Enter to capture mouse position.")
                self.capture_mode = False  # Switch to capture mode
                self.record_mode = False
        else:
            # Capture mouse position
            x, y = pyautogui.position()
            self.status_label.config(text=f"Captured ({x}, {y}) for '{key}'")

            data = {}
            try:
                with open('scripts/locations.json', 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                pass

            if key in data[category]:
                data[category][key]["coordinates"] = [x, y]
            else:
                data[category][key] = {"coordinates": [x, y], "description": "tbc"}

            with open('scripts/locations.json', 'w') as f:
                json.dump(data, f, indent=4)

            self.display_location_keys()

            self.capture_mode = True  # Switch back to key confirmation mode

if __name__ == "__main__":
    root = tk.Tk()
    app = CalibrationApp(root)
    root.mainloop()
