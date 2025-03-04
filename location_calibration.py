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

        self.capture_mode = True  # Flag to toggle between modes

        self.selected_category.trace('w', self.display_location_keys)

        self.root.bind('<Return>', self.on_enter)  # Bind Enter key to on_enter method

    def display_location_keys(self, *args):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        with open("scripts/locations.json", "r") as f:
            locations = json.load(f)
        self.output_text.insert(tk.END, f"Keys for '{self.selected_category.get()}':\n")
        for key in locations[self.selected_category.get()].keys():
            self.output_text.insert(tk.END, f"{key}: {locations[self.selected_category.get()][key]}\n")
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
                self.status_label.config(text=f"'{key}' not in '{category}'")
            else:
                self.status_label.config(text=f"Location: '{key}'confirmed.\nPress Enter to capture mouse position.")
                self.capture_mode = False  # Switch to capture mode
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

            data[category][key] = [x, y]

            with open('scripts/locations.json', 'w') as f:
                json.dump(data, f, indent=4)

            self.display_location_keys()

            self.capture_mode = True  # Switch back to key confirmation mode

if __name__ == "__main__":
    root = tk.Tk()
    app = CalibrationApp(root)
    root.mainloop()
