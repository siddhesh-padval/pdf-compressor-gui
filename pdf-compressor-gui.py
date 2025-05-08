import tkinter as tk
from tkinter import filedialog
import subprocess
import os

class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Compressor (Ghostscript GUI)")

        # Input PDF
        tk.Label(root, text="Input PDF:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.open_custom_file_browser).grid(row=0, column=2, padx=5)

        # Quality Preset
        tk.Label(root, text="Quality Preset:").grid(row=1, column=0, sticky="e", padx=5)
        self.quality_preset = tk.StringVar(value="custom")
        preset_menu = tk.OptionMenu(root, self.quality_preset, "custom", "screen", "ebook", "printer", "prepress", "default", command=self.update_resolutions)
        preset_menu.grid(row=1, column=1, sticky="w", padx=5)

        # Image Resolutions
        tk.Label(root, text="Color Image Resolution:").grid(row=2, column=0, sticky="e", padx=5)
        self.color_res = tk.Entry(root)
        self.color_res.grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(root, text="Gray Image Resolution:").grid(row=3, column=0, sticky="e", padx=5)
        self.gray_res = tk.Entry(root)
        self.gray_res.grid(row=3, column=1, sticky="w", padx=5)

        tk.Label(root, text="Mono Image Resolution:").grid(row=4, column=0, sticky="e", padx=5)
        self.mono_res = tk.Entry(root)
        self.mono_res.grid(row=4, column=1, sticky="w", padx=5)

        # Compatibility Level
        tk.Label(root, text="PDF Compatibility Level:").grid(row=5, column=0, sticky="e", padx=5)
        self.compat_level = tk.StringVar(value="1.4")
        tk.OptionMenu(root, self.compat_level, "1.3", "1.4", "1.5", "1.6", "1.7").grid(row=5, column=1, sticky="w", padx=5)

        # Buttons
        tk.Button(root, text="Compress PDF", bg="green", fg="white", command=self.compress_pdf).grid(row=6, column=0, pady=10, padx=5)
        tk.Button(root, text="Restore Defaults", command=self.restore_defaults).grid(row=6, column=1, pady=10, sticky="w")

        # Status message
        self.status_message = tk.Message(root, text="", fg="blue", width=500, anchor="w", justify="left")
        self.status_message.grid(row=7, column=0, columnspan=3, pady=(5, 10), padx=5)

        self.restore_defaults()

    def open_custom_file_browser(self):
        top = tk.Toplevel(self.root)
        top.title("Select PDF File")
        top.geometry("600x400")

        frame = tk.Frame(top)
        frame.pack(fill="both", expand=True)

        listbox = tk.Listbox(frame, width=100)
        listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)

        current_dir = os.path.expanduser("~")

        def update_listbox(directory):
            listbox.delete(0, tk.END)
            try:
                entries = os.listdir(directory)
                entries.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower()))
            except PermissionError:
                return

            if os.path.dirname(directory) != directory:
                listbox.insert(tk.END, "..")

            for entry in entries:
                full_path = os.path.join(directory, entry)
                if os.path.isdir(full_path):
                    listbox.insert(tk.END, f"[DIR] {entry}")
                elif entry.lower().endswith(".pdf"):
                    listbox.insert(tk.END, entry)

        def on_select(event):
            selection = listbox.curselection()
            if selection:
                selected = listbox.get(selection[0])
                nonlocal current_dir

                if selected == "..":
                    current_dir = os.path.dirname(current_dir)
                    update_listbox(current_dir)
                elif selected.startswith("[DIR] "):
                    dir_name = selected[6:]
                    current_dir = os.path.join(current_dir, dir_name)
                    update_listbox(current_dir)
                else:
                    file_path = os.path.join(current_dir, selected)
                    self.input_entry.delete(0, tk.END)
                    self.input_entry.insert(0, file_path)
                    top.destroy()

        listbox.bind("<Double-Button-1>", on_select)

        update_listbox(current_dir)

    def restore_defaults(self):
        self.quality_preset.set("custom")
        for entry, val in zip((self.color_res, self.gray_res, self.mono_res), (200, 200, 200)):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(val))
        self.compat_level.set("1.4")
        self.status_message.config(text="Defaults restored.", fg="blue")

    def update_resolutions(self, value):
        presets = {
            "screen": (72, 72, 72),
            "ebook": (150, 150, 150),
            "printer": (300, 300, 300),
            "prepress": (300, 300, 300),
            "default": (300, 300, 300),
            "custom": (200, 200, 200)
        }

        res = presets.get(value, (200, 200, 200))
        for entry, val in zip((self.color_res, self.gray_res, self.mono_res), res):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

    def compress_pdf(self):
        input_pdf = self.input_entry.get().strip()
        if not os.path.isfile(input_pdf):
            self.status_message.config(text="Error: Invalid input PDF.", fg="red")
            return

        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        quality = self.quality_preset.get()
        output_pdf = os.path.join(os.path.dirname(input_pdf), f"{base_name}_compressed_{quality}.pdf")

        cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            f"-dCompatibilityLevel={self.compat_level.get()}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf}",
            input_pdf
        ]

        if quality != "custom":
            cmd.insert(-2, f"-dPDFSETTINGS=/{quality}")
        else:
            cmd.extend([
                "-dDownsampleColorImages=true",
                "-dDownsampleGrayImages=true",
                "-dDownsampleMonoImages=true",
                f"-dColorImageResolution={self.color_res.get()}",
                f"-dGrayImageResolution={self.gray_res.get()}",
                f"-dMonoImageResolution={self.mono_res.get()}",
            ])

        try:
            subprocess.run(cmd, check=True)
            orig_size = os.path.getsize(input_pdf)
            comp_size = os.path.getsize(output_pdf)

            def readable_size(size_bytes):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size_bytes < 1024.0:
                        return f"{size_bytes:.2f} {unit}"
                    size_bytes /= 1024.0
                return f"{size_bytes:.2f} TB"

            msg = (
                f"Compression Successful!\n\n"
                f"Saved to: {output_pdf}\n"
                f"Original Size: {readable_size(orig_size)}\n"
                f"Compressed Size: {readable_size(comp_size)}"
            )
            self.status_message.config(text=msg, fg="green")
        except subprocess.CalledProcessError:
            self.status_message.config(text="Compression failed. Check Ghostscript installation.", fg="red")
        except FileNotFoundError:
            self.status_message.config(text="Ghostscript not found. Please install and add to PATH.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
