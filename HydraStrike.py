import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import os
import threading

running = False

def run_hydra(user_input, pass_list, target_ip, method, incorrect_verbiage):
    global running
    running = True
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)

    if os.path.isfile(user_input):
        user_list_option = f"-L {user_input}"
    else:
        user_list_option = f"-l {user_input}"

    if not os.path.isfile(pass_list):
        output_text.insert(tk.END, f"[!] Password list file not found: {pass_list}\n")
        output_text.config(state=tk.DISABLED)
        return

    command = f"sudo hydra {user_list_option} -P {pass_list} {target_ip} http-post-form \"{method}:username=^USER^&password=^PASS^&Login=Login:{incorrect_verbiage}\""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_lines = 100  # Estimated for progress
        line_count = 0
        while running:
            line = process.stdout.readline()
            if not line:
                break
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            line_count += 1
            progress['value'] = min((line_count / total_lines) * 100, 100)
            root.update_idletasks()
            if "login:" in line:
                output_text.insert(tk.END, "\n[+] Login found. Stopping further attempts.\n")
                process.terminate()
                break

        stderr_output = process.stderr.read()
        if stderr_output:
            output_text.insert(tk.END, stderr_output)

        with open("hydrastrike_output.txt", "w") as f:
            f.write(output_text.get(1.0, tk.END))

    except Exception as e:
        output_text.insert(tk.END, f"\n[!] Error: {e}\n")

    output_text.config(state=tk.DISABLED)
    progress['value'] = 0


def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)

def start_hydra():
    t = threading.Thread(target=run_script)
    t.start()

def stop_hydra():
    global running
    running = False

def run_script():
    user_input = entry_user_input.get()
    pass_list = entry_passlist.get()
    target_ip = entry_target_ip.get()
    method = entry_method.get()
    incorrect_verbiage = entry_incorrect_verbiage.get()

    run_hydra(user_input, pass_list, target_ip, method, incorrect_verbiage)

def apply_theme():
    theme = theme_var.get()
    colors = {
        "light": {
            "bg": "lightgrey",
            "fg": "black",
            "entry_bg": "white",
            "entry_fg": "black",
            "output_fg": "black"
        },
        "dark": {
            "bg": "#2e2e2e",
            "fg": "white",
            "entry_bg": "#4d4d4d",
            "entry_fg": "white",
            "output_fg": "#90ee90"
        }
    }

    selected = colors[theme]
    root.configure(bg=selected["bg"])

    for widget in root.winfo_children():
        cls = widget.__class__.__name__
        if cls == "Label" or cls == "Button":
            widget.configure(bg=selected["bg"], fg=selected["fg"])
        elif cls == "Entry":
            widget.configure(bg=selected["entry_bg"], fg=selected["entry_fg"])
        elif cls == "Text":
            widget.configure(bg=selected["entry_bg"], fg=selected["output_fg"])

# === GUI STARTS HERE ===
root = tk.Tk()
root.title("HydraStrike")

# Theme
theme_var = tk.StringVar(value="light")
tk.Label(root, text="Theme:").grid(row=0, column=0)
theme_menu = ttk.Combobox(root, textvariable=theme_var, values=["light", "dark"], state="readonly")
theme_menu.grid(row=0, column=1)
btn_theme = tk.Button(root, text="Apply Theme", command=apply_theme)
btn_theme.grid(row=0, column=2)

# Username
tk.Label(root, text="Username or User List Path:").grid(row=1, column=0)
entry_user_input = tk.Entry(root)
entry_user_input.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_user_input)).grid(row=1, column=2)

# Password List
tk.Label(root, text="Password List:").grid(row=2, column=0)
entry_passlist = tk.Entry(root)
entry_passlist.grid(row=2, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(entry_passlist)).grid(row=2, column=2)

# Target IP
tk.Label(root, text="Target IP:").grid(row=3, column=0)
entry_target_ip = tk.Entry(root)
entry_target_ip.grid(row=3, column=1)

# Method Path
tk.Label(root, text="Method (Path):").grid(row=4, column=0)
entry_method = tk.Entry(root)
entry_method.grid(row=4, column=1)

# Incorrect Verbiage
tk.Label(root, text="Incorrect Verbiage:").grid(row=5, column=0)
entry_incorrect_verbiage = tk.Entry(root)
entry_incorrect_verbiage.grid(row=5, column=1)

# Run and Stop Buttons
tk.Button(root, text="Start Hydra", command=start_hydra).grid(row=6, column=0)
tk.Button(root, text="Stop", command=stop_hydra).grid(row=6, column=1)

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.grid(row=7, column=0, columnspan=3, pady=10)

# Output Box
output_text = tk.Text(root, height=15, width=100, state=tk.DISABLED)
output_text.grid(row=8, column=0, columnspan=3)

apply_theme()
root.mainloop()

