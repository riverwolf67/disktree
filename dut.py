#!/usr/bin/python
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
        try:
            if os.path.isdir(full_path) and not os.path.islink(full_path):
                size = get_size(full_path)
            else:
                size = os.path.getsize(full_path)
        except (FileNotFoundError, OSError):
            size = 0
        items.append((item, size))

    # Sort by size descending
    items.sort(key=lambda x: x[1], reverse=True)
    
    max_size = items[0][1] if items else 1

    min_size = 100 * 1024 * 1024  # 100 MB

    for name, size in items:
        if size < min_size:
            continue
        relative_size = size / max_size
        bar_length = int(relative_size * bar_max_width)
        bar = "█" * bar_length
        print(f"{name[:20]:<20} | {format_size(size):>10} | {bar}")

    print(f"\n(Items less than 100 MB are not shown)")

if __name__ == "__main__":
    main()
