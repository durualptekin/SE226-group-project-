import json
import os
import tkinter as tk
from tkinter import filedialog

def export_album(album_data, cover_image = None):
    """Makes the user choose an file to save the data."""
    root = tk.Tk()
    root.withdraw()

    print("Opening the file selection window...")
    folder_path = filedialog.askdirectory(title="Choose a file to save the album.")

    if folder_path:
        json_file_path = os.path.join(folder_path, "album_info.json")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(album_data, f, indent=4, ensure_ascii=False)
        
        if cover_image:
            png_file_path = os.path.join(folder_path, "album_cover.png")
            cover_image.save(png_file_path, format="PNG")

        print(f"Files have been saved to {folder_path}")
    else:
        print("Task is cancelled, no file is choosen.")

