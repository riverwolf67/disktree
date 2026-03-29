# disktree.py
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
