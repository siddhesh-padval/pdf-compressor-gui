# PDF Compressor GUI (Ghostscript Frontend)

A simple, cross-platform Python GUI to compress PDF files using Ghostscript.

## 📷 Features

- Compress any PDF using Ghostscript via a user-friendly interface
- Adjust resolution for:
  - Color Images
  - Grayscale Images
  - Monochrome Images
- Choose PDF compatibility level (`1.3` to `1.7`)
- Use built-in quality presets: `screen`, `ebook`, `printer`, `prepress`
- Restore default settings with one click

## 🚀 Getting Started

### 📦 Requirements

- Python 3.x
- [Ghostscript](https://www.ghostscript.com/) installed and available in your system PATH
- Tkinter (pre-installed with most Python distributions)

### ✅ Linux (Ubuntu/Debian)

```bash
sudo apt-get install ghostscript python3-tk
```

### ✅ Windows

1. Install [Ghostscript](https://www.ghostscript.com/download/gsdnld.html) and add it to your PATH
2. Make sure Python is installed with Tkinter

### 🏃 Run the App

```bash
python3 gscompressor.py
```

---

## 🖼️ Screenshots

> _(Add screenshots of the GUI here later)_

---

## 🔧 Preset Options

| Preset   | Color / Gray DPI | Mono DPI | Use Case                    |
|----------|------------------|----------|-----------------------------|
| screen   | 72               | 72       | Minimal size                |
| ebook    | 150              | 150      | E-book readers              |
| printer  | 300              | 300      | High-quality print output   |
| prepress | 300              | 1200     | Professional publishing     |

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.
