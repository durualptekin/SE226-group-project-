import tkinter as tk
import threading
import time

from ui_components import AlbumCoverStudioUI
from export_logic import export_album
from media_utils import create_placeholder_image, convert_to_tk_image
from image_engine import generate_cover_image
# from ai_engine import ... (Commented until ai_engine.py is filled)
# from music_service import ... (Commented until music_service.py is filled)

class SystemController:
    def __init__(self, root):
        self.root = root
        
        #  Getting the ip of the buttons by hand when starting UI
    
        self.ui = AlbumCoverStudioUI(
            root,
            on_generate_callback=self.start_generation_thread,
            on_save_callback=self.save_album_logic
        )
        
        #  Holding the generated data to be able to use when save button is pressed
        self.current_metadata = None
        self.current_tracklist = None
        self.current_image = None

    def start_generation_thread(self, mood, genre, era, track_count):
        """Making UI not to freeze when pending."""
        self.ui.generate_btn.config(state="disabled")
        
        thread = threading.Thread(
            target=self.orchestrate_pipeline,
            args=(mood, genre, era, track_count)
        )
        thread.start()

    def orchestrate_pipeline(self, mood, genre, era, track_count):
        """Main data line where all modules are called(Data Pipe)."""
        
        # 1st step: Gemini API (Fake waits for now)
        self.root.after(0, lambda: self.ui.status_label.config(text="Gemini is thinking..."))
        time.sleep(2) 
        
        # 2nd step: Last.fm API (fake waits for now)
        self.root.after(0, lambda: self.ui.status_label.config(text="Fetching tracks from Last.fm..."))
        time.sleep(2)
        
       # 3rd step: Image generation
        self.root.after(0, lambda: self.ui.status_label.config(text="Generating cover art..."))
        
        try:
            # fake description for now
            mock_cover_prompt = "A beautiful sunset over the Aegean sea, melancholic"
            
            real_pil_image = generate_cover_image(cover_prompt=mock_cover_prompt, genre=genre)
            self.current_image = real_pil_image
            
            # formatting the image
            tk_image = convert_to_tk_image(real_pil_image, size=(300, 300))
            self.root.after(0, lambda: self.ui.update_cover_image(tk_image))
            
        except Exception as e:
            # Placeholder incase network connection is lost
            print(f"Could not download the image: {e}")
            placeholder_pil = create_placeholder_image(text="Image\nFailed", background="red")
            tk_image = convert_to_tk_image(placeholder_pil, size=(300, 300))
            self.root.after(0, lambda: self.ui.update_cover_image(tk_image))
        
        time.sleep(1)

        # Placeholder fake data 
        self.current_metadata = {
            "album_name": "Ghost Reveries",
            "artist_name": "Opeth",
            "year": era.replace("s", ""),
            "genre": genre,
            "label": "..."
        }
        self.current_tracklist = [
            {"name": f"Test song {i+1}", "artist": "Radiohead", "url": "https://www.last.fm"} 
            for i in range(track_count)
        ]

        # 4th step: UI update
        self.root.after(0, lambda: self.ui.update_ui_with_data(self.current_metadata, self.current_tracklist))
        self.root.after(0, lambda: self.ui.status_label.config(text="Album is ready!"))
        self.root.after(0, lambda: self.ui.generate_btn.config(state="normal"))

    def save_album_logic(self):
        """Works when the user presses 'save' button and sends the data to export_logic module."""
        if self.current_metadata and self.current_tracklist:
            full_data = {
                "album_info": self.current_metadata,
                "tracks": self.current_tracklist
            }
            
            export_album(full_data, cover_image=self.current_image)
        else:
            print("No album to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemController(root)
    root.mainloop()
