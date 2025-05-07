import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

# Preset values for resolution based on Ghostscript settings
PRESET_VALUES = {
    "screen":    (72, 72, 72),
    "ebook":     (150, 150, 150),
    "printer":   (300, 300, 300),
    "prepress":  (300, 300, 1200),
    "default":   (200, 200, 200)
}

def apply_preset(preset):
    res = PRESET_VALUES.get(preset, PRESET_VALUES["default"])
    color_res.set(res[0])
    gray_res.set(res[1])
    mono_res.set(res[2])

def restore_defaults():
    color_res.set(200)
    gray_res.set(200)
    mono_res.set(200)
    compat_level.set("1.4")
    preset_choice.set("custom")

def compress_pdf(input_path, output_path, color, gray, mono, compat):
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        f'-dCompatibilityLevel={compat}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dDownsampleColorImages=true',
        f'-dColorImageResolution={color}',
        '-dDownsampleGrayImages=true',
        f'-dGrayImageResolution={gray}',
        '-dDownsampleMonoImages=true',
        f'-dMonoImageResolution={mono}',
        f'-sOutputFile={output_path}',
        input_path
    ]
    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Compressed PDF saved to:\n{output_path}")

    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Compression failed. Make sure Ghostscript is installed and in your PATH.")

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def run_compression():
    input_path = input_entry.get()
    output_path = output_entry.get()

    if not input_path or not output_path:
        messagebox.showwarning("Input Required", "Please select both input and output files.")
        return

    compress_pdf(
        input_path,
        output_path,
        color_res.get(),
        gray_res.get(),
        mono_res.get(),
        compat_level.get()
    )

# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Compressor (Ghostscript GUI)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# File selection
tk.Label(frame, text="Input PDF:").grid(row=0, column=0, sticky='e')
input_entry = tk.Entry(frame, width=50)
input_entry.grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_input_file).grid(row=0, column=2)

tk.Label(frame, text="Output PDF:").grid(row=1, column=0, sticky='e')
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1)
tk.Button(frame, text="Browse", command=select_output_file).grid(row=1, column=2)

# Preset selector
tk.Label(frame, text="Quality Preset:").grid(row=2, column=0, sticky='e')
preset_choice = tk.StringVar(value="custom")
preset_menu = ttk.Combobox(frame, textvariable=preset_choice, state="readonly",
                           values=["custom", "screen", "ebook", "printer", "prepress"])
preset_menu.grid(row=2, column=1, sticky='w')

def on_preset_change(event):
    preset = preset_choice.get()
    if preset != "custom":
        apply_preset(preset)

preset_menu.bind("<<ComboboxSelected>>", on_preset_change)

# Compression options
tk.Label(frame, text="Color Image Resolution:").grid(row=3, column=0, sticky='e')
color_res = tk.IntVar(value=200)
tk.Entry(frame, textvariable=color_res, width=10).grid(row=3, column=1, sticky='w')

tk.Label(frame, text="Gray Image Resolution:").grid(row=4, column=0, sticky='e')
gray_res = tk.IntVar(value=200)
tk.Entry(frame, textvariable=gray_res, width=10).grid(row=4, column=1, sticky='w')

tk.Label(frame, text="Mono Image Resolution:").grid(row=5, column=0, sticky='e')
mono_res = tk.IntVar(value=200)
tk.Entry(frame, textvariable=mono_res, width=10).grid(row=5, column=1, sticky='w')

tk.Label(frame, text="PDF Compatibility Level:").grid(row=6, column=0, sticky='e')
compat_level = tk.StringVar(value="1.4")
compat_dropdown = ttk.Combobox(frame, textvariable=compat_level,
                                values=["1.3", "1.4", "1.5", "1.6", "1.7"],
                                width=8, state="readonly")
compat_dropdown.grid(row=6, column=1, sticky='w')

# Buttons
button_frame = tk.Frame(frame)
button_frame.grid(row=7, column=0, columnspan=3, pady=15)

tk.Button(button_frame, text="Compress PDF", command=run_compression, bg="green", fg="white", padx=10).pack(side='left', padx=5)
tk.Button(button_frame, text="Restore Defaults", command=restore_defaults, bg="gray", fg="white", padx=10).pack(side='left', padx=5)

root.mainloop()
