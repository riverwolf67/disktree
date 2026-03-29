# README.md

disktree is a sh cli tool to show a **bar-graph distribution** (like [filelight](https://github.com/kde/filelight)) info in linux shell / terminal.

Displaying visual disk usage (similar to Filelight’s radial map) directly in a Bash terminal is best handled using a Python script, as it allows for easier calculation of terminal widths and color formatting.

While tools like `dust` or `ncdu` are the standard CLI equivalents, here is a custom Python script that generates a **bar-graph distribution** of directory sizes.

## Alternatives

If you are looking for a highly polished, interactive "Filelight-style" experience without writing custom code, these tools are built specifically for the terminal:

* **`[ncdu](https://dev.yorhel.nl/ncdu)`**: The "Gold Standard" for CLI disk usage. It provides an interactive interface to navigate folders and delete files.
* **`[dust](https://github.com/bootandy/dust)`**: A modern version of `du` written in Rust that provides a tree-like visual overview with colored bars automatically.
* **`[vizex](https://github.com/bexxmodd/vizex)`**: A Python-based tool specifically designed to show disk usage with graphs in the terminal.

### The Python Script (`disktree.py`)

This script traverses the current directory, calculates sizes, and renders a visual representation.

```python
import os
import shutil

def get_size(start_path='.'):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except (PermissionError, FileNotFoundError):
        return 0
    return total_size

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def main():
    path = "."
    items = []
    
    # Get terminal width for the bar
    cols, _ = shutil.get_terminal_size()
    bar_max_width = cols - 50 

    print(f"\n--- Disk Usage: {os.path.abspath(path)} ---\n")

    # Analyze immediate subdirectories and files
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        size = get_size(full_path) if os.path.isdir(full_path) else os.path.getsize(full_path)
        items.append((item, size))

    # Sort by size descending
    items.sort(key=lambda x: x[1], reverse=True)
    
    max_size = items[0][1] if items else 1

    for name, size in items:
        relative_size = size / max_size
        bar_length = int(relative_size * bar_max_width)
        bar = "█" * bar_length
        print(f"{name[:20]:<20} | {format_size(size):>10} | {bar}")

if __name__ == "__main__":
    main()
```

---

### How to use it
1. Save the code as `disktree.py`.
2. Run it with: `python3 disktree.py`.
3. It will scan the current directory and output a sorted list with a visual bar representing the weight of each folder/file.
