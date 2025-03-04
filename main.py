import os
import subprocess
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
from scripts.utils_hidden import format_time

global process
process = None

def run_script(script_name):
    """Runs the selected script in a separate thread and captures output in real time."""
    global process
    if process is not None:
        return  # Prevent running multiple scripts at once
    
    stop_button.config(state=tk.NORMAL)  # Enable stop button
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"\n--- Running {script_name} ---\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)
    
    def target():
        global process
        process = subprocess.Popen(
            ["python", os.path.join("scripts", script_name)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True
        )
        
        def read_output(pipe):
            """Reads output line by line and updates the text box."""
            while True:
                line = pipe.readline()
                if not line:
                    break
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, line)
                output_text.config(state=tk.DISABLED)
                output_text.see(tk.END)
            pipe.close()
        
        stdout_thread = threading.Thread(target=read_output, args=(process.stdout,))
        stderr_thread = threading.Thread(target=read_output, args=(process.stderr,))
        stdout_thread.start()
        stderr_thread.start()
        global start_time
        start_time = time.time()
        
        stdout_thread.join()
        stderr_thread.join()
        
        if process:
            process.wait()
        process = None
        stop_button.config(state=tk.DISABLED)  # Disable stop button
    
    thread = threading.Thread(target=target, daemon=True)
    thread.start()

def stop_script():
    """Stops the currently running script."""
    global process
    if process is not None:
        process.terminate()
        process = None
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"\n--- Script Terminated ---\nScript ran for {format_time(time.time()-start_time)}\n")
        output_text.config(state=tk.DISABLED)
        output_text.see(tk.END)
    stop_button.config(state=tk.DISABLED)  # Disable stop button

def quit_app():
    """Stops any running script and exits the application."""
    stop_script()
    root.quit()
    root.destroy()

# Create main window
root = tk.Tk()
root.title("Script Runner")
root.geometry("350x400")
root.attributes("-topmost", True)  # Make window always stay on top

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Output log
output_text = ScrolledText(root, wrap=tk.WORD, height=15, state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# List scripts and create buttons
script_folder = "scripts"
os.makedirs(script_folder, exist_ok=True)  # Ensure folder exists

script_files = [f for f in os.listdir(script_folder) if f.endswith(".py") and not f.endswith("_hidden.py")]

for script in script_files:
    try:
        btn = tk.Button(button_frame, text=script, command=lambda s=script: run_script(s))
        btn.pack(side=tk.LEFT, padx=5, pady=5)
        print(f"Successfully imported {script}")
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Failed to import {script}: {e}")
    

# Stop button
stop_button = tk.Button(root, text="Stop Script", command=stop_script, state=tk.DISABLED)
stop_button.pack(pady=5)

# Quit button
quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", quit_app)  # Ensure proper cleanup on window close

root.mainloop()
