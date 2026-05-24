import tkinter as tk
from tkinter import ttk
import webbrowser


class AlbumCoverStudioUI:

    def __init__(self, root, on_generate_callback=None,on_save_callback= None ):

        self.root= root
        self.on_generate_callback= on_generate_callback
        self.on_save_callback= on_save_callback
        self.root.title("Album Cover Studio")
        self.root.geometry("1100x700")
        self.root.minsize(900,600)

        self.bg_color= "#121212"
        self.fg_color= "#FFFFFF"
        self.accent_color= "#1DCD5B"
        self.secondary_bg= "#2E2D2D"
        
        self.root.configure(bg=self.bg_color)

        style= ttk.Style()
        style.theme_use('clam')

        style.configure("TFrame",background= self.bg_color)
        style.configure("TLabel",background= self.bg_color, foreground=self.fg_color)

        style.configure("Accent.TButton",background= self.accent_color, foreground="white", font=("Helvetica",10,"bold"), borderwidth=0)
        style.map("Accent.TButton",background=[("active", "#1ade5f")])

        style.configure("Secondary.TButton",background= self.secondary_bg, foreground="white", font=("Helvetica",9))
        style.map("Secondary.TButton",background=[("active", "#3E3E3E")])

        self.main_container= ttk.Frame(self.root)
        self.main_container.pack(fill= tk.BOTH, expand=True)


        self.left_frame =ttk.Frame(self.main_container, width=350)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        self.left_frame.pack_propagate(False)

        self.right_frame= ttk.Frame(self.main_container)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,20),pady=20)

        self._build_input_section()
        self._build_output_section()



    def _build_input_section(self):

        ttk.Label(self.left_frame, text="Your Mood (English or Turkish): ", font=("Helvetica",10, "bold")).pack(anchor="w", pady=(0,5)) 

        self.journal_text= tk.Text(self.left_frame, height=8, wrap=tk.WORD, font=("Helvetica", 10), relief="flat", highlightthickness=1, bg=self.secondary_bg,fg=self.fg_color, insertbackground="white")
        self.journal_text.pack(fill=tk.X, pady=(0,15))

        default_mood= "I was looking at the sea in Izmir. It was raining softly, and an old song was playing through my headphones. I felt both peaceful and melancholic..."
        self.journal_text.insert(tk.END,default_mood)

        ttk.Label(self.left_frame, text="Genre: ", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.genre_var= tk.StringVar()
        self.genre_combo= ttk.Combobox(self.left_frame, textvariable=self.genre_var, state="readonly")
        self.genre_combo['values']= ("Pop", "Rock" , "Hip-Hop/Rap","Electronic","Indie","R&B/Soul","Jazz","Metal", "Türk Pop","Klasik" )
        self.genre_combo.set("Indie")
        self.genre_combo.pack(fill=tk.X, pady=(0,15))

        ttk.Label(self.left_frame, text="Era: ", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.era_var= tk.StringVar()
        self.era_combo= ttk.Combobox(self.left_frame, textvariable=self.era_var, state="readonly")
        self.era_combo['values']= ("1970s", "1980s", "1990s", "2000s", "2010s", "2020s")
        self.era_combo.set("2000s")
        self.era_combo.pack(fill= tk.X, pady=(0,15))

        ttk.Label(self.left_frame, text="Track count: ", font=("Helvetica", 10, "bold")).pack(anchor="w")
        self.track_count_var= tk.IntVar(value=10)
        self.track_spinbox= ttk.Spinbox(self.left_frame, from_=6, to=14 , textvariable=self.track_count_var, state="readonly")
        self.track_spinbox.pack(fill= tk.X, pady=(0,25))

        self.generate_btn = ttk.Button(self.left_frame, text="GENERATE ALBUM",style="Accent.TButton" ,command=self.on_generate_click)
        self.generate_btn.pack(fill= tk.X, ipady=8)


    
    def on_generate_click(self):

        user_mood= self.journal_text.get("1.0", tk.END).strip()
        selected_genre= self.genre_var.get()
        selected_era= self.era_var.get()
        selected_track_count= self.track_count_var.get()


        self.status_label.config(text="Processing... Please wait.")


        if self.on_generate_callback:
            self.on_generate_callback(user_mood, selected_genre,selected_era, selected_track_count)

        else:

            print("--- Mock Album Generation Triggered ---")

            mock_metadata= {
            "album_name": "Echoes of the Aegean",
            "artist_name": "The Kordon Wanderers",
            "year": selected_era.replace("s", ""),
            "genre": selected_genre,
            "label": "Izmir Records"
        }
            
        mock_tracklist = [{"name": f"Melancholy Track {i+1}", "artist": "Various Indie Artists", "url": "https://www.last.fm"} for i in range(selected_track_count)]
        self.update_ui_with_data(mock_metadata, mock_tracklist)
        self.status_label.config(text="Album generated successfully!")

        
        

    def on_generate_click(self):

        user_mood= self.journal_text.get("1.0", tk.END).strip()
        selected_genre= self.genre_var.get()
        selected_era= self.era_var.get()
        selected_track_count= self.track_count_var.get()

        self.status_label.config(text="Processing... Please wait.")

        if self.on_generate_callback:
            self.on_generate_callback(user_mood, selected_genre,selected_era, selected_track_count)
            return

        print("--- Mock Album Generation Triggered ---")

        mock_metadata= {
        "album_name": "Echoes of the Aegean",
        "artist_name": "The Kordon Wanderers",
        "year": selected_era.replace("s", ""),
        "genre": selected_genre,
        "label": "Izmir Records"
        }
            
        mock_tracklist = [{"name": f"Melancholy Track {i+1}", "artist": "Various Indie Artists", "url": "https://www.last.fm"} for i in range(selected_track_count)]
        self.update_ui_with_data(mock_metadata, mock_tracklist)
        self.status_label.config(text="Album generated successfully!")


    def _build_output_section(self):

        self.header_frame= ttk.Frame(self.right_frame)
        self.header_frame.pack(fill= tk.X, pady=(0,20))

        self.cover_label= tk.Label(self.header_frame, text="Album Cover\n(Loading...)", bg= "#333333", fg= "white", width=25, height=12) 
        self.cover_label.pack(side=tk.LEFT, padx=(0,20))

        self.meta_frame= ttk.Frame(self.header_frame)
        self.meta_frame.pack(side=tk.LEFT, fill= tk.BOTH, expand=True)

        self.album_title_label = tk.Label(self.meta_frame, text="Album Title", bg=self.bg_color, fg=self.fg_color,font=("Helvetica", 28, "bold"), anchor="w")
        self.album_title_label.pack(fill=tk.X)

        self.artist_title_label = tk.Label(self.meta_frame, text="Artist Name",bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 16), anchor="w")
        self.artist_title_label.pack(fill=tk.X, pady=(5,10))

        self.details_label = tk.Label(self.meta_frame, text="Year * Genre * Label",bg=self.bg_color, font=("Helvetica", 10, "italic"),fg= "gray" , anchor="w")
        self.details_label.pack(fill=tk.X)

        self.tracklist_container= ttk.Frame(self.right_frame)
        self.tracklist_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.tracklist_container, highlightthickness=0 ,bg=self.bg_color)
        self.scrollbar= ttk.Scrollbar(self.tracklist_container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame= ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_window= self.canvas.create_window((0,0), window=self.scrollable_frame, anchor= "nw")

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width= e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT,fill= tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.save_btn= ttk.Button(self.right_frame, text="SAVE ALBUM (JSON+PNG)", style="Accent.TButton", state="disabled", command=self.on_save_callback)
        self.save_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,5),ipady=5)

        self.status_label= tk.Label(self.right_frame, text="Ready. Describe your mood to generate an album.",bg=self.bg_color, font=("Helvetica", 10),fg= "gray" , anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10,0))


    def update_ui_with_data(self, album_metadata, tracklist):

        self.album_title_label.config(text=album_metadata.get("album_name", "Unknown Album"))
        self.artist_title_label.config(text=album_metadata.get("artist_name", "Unknown Artist" ))

        year = album_metadata.get("year", "202X")
        genre = album_metadata.get("genre", self.genre_var.get())
        label = album_metadata.get("label", "Independent")
        self.details_label.config(text=f"{year} * {genre} * {label}")

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, track in enumerate(tracklist, start=1):

            track_row= ttk.Frame(self.scrollable_frame)
            track_row.pack(fill=tk.X, pady=5, padx=10)

            num_label= tk.Label(track_row, text=str(index), width=3,bg=self.bg_color, fg="gray")
            num_label.pack(side=tk.LEFT)

            info_frame= ttk.Frame(track_row)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            tk.Label(info_frame, text=track.get("name", "Unknown Track"),bg=self.bg_color ,fg=self.fg_color, font=("Helvetica", 11, "bold"), anchor="w").pack(fill=tk.X)
            tk.Label(info_frame, text=track.get("artist", "Unknown Artist"),bg=self.bg_color, font=("Helvetica", 9, "bold"),fg="gray",  anchor="w").pack(fill=tk.X)

            track_url= track.get("url", "")
            listen_btn= ttk.Button(track_row, text="Listen", style="Secondary.TButton", command= lambda url=track_url: webbrowser.open(url) if url else None)
            listen_btn.pack(side=tk.RIGHT)

        self.save_btn.config(state="normal")



    def update_cover_image(self, photo_image):

        if photo_image:
            self.cover_label.config(image=photo_image, text="")
            self.cover_label.image= photo_image


if __name__ == "__main__":

    root = tk.Tk()
    app= AlbumCoverStudioUI(root)
    root.mainloop()
