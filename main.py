import customtkinter as ctk
import yt_dlp
import threading
import os
from tkinter import messagebox, filedialog

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Youtube Downloader - MarcausenteDev")
        self.geometry("600x450")
        
        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Spacer row

        # Title
        self.title_label = ctk.CTkLabel(self, text="Youtube Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # URL Input
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="Pega el enlace de YouTube aquí...")
        self.url_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Folder Selection
        self.folder_frame = ctk.CTkFrame(self)
        self.folder_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.folder_frame.grid_columnconfigure(1, weight=1)

        self.select_folder_btn = ctk.CTkButton(self.folder_frame, text="Carpeta", command=self.select_folder, width=80)
        self.select_folder_btn.grid(row=0, column=0, padx=10, pady=10)

        self.folder_path_label = ctk.CTkLabel(self.folder_frame, text="No se ha seleccionado carpeta", text_color="gray")
        self.folder_path_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.selected_folder = ""

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Descargar Video", command=self.confirmar_descarga, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.download_btn.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Progress Bar and Status
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progress_bar.set(0)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            # Truncate path if too long for display
            display_text = folder if len(folder) < 40 else "..." + folder[-37:]
            self.folder_path_label.configure(text=display_text, text_color=("black", "white"))

    def confirmar_descarga(self):
        url = self.url_entry.get()
        
        if not url:
            self.status_label.configure(text="⚠ Por favor introduce una URL", text_color="red")
            return
            
        if not self.selected_folder:
            self.status_label.configure(text="⚠ Por favor selecciona una carpeta", text_color="red")
            return

        self.download_btn.configure(state="disabled", text="Descargando...")
        self.status_label.configure(text="Iniciando descarga...", text_color=("black", "white"))
        self.progress_bar.set(0)
        
        # Run in thread
        thread = threading.Thread(target=self.descargar_video, args=(url, self.selected_folder))
        thread.start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%', '')
                progress = float(p) / 100
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Descargando: {d.get('_percent_str', '0%')}", text_color=("black", "white"))
                self.update_idletasks()
            except ValueError:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.set(1)
            self.status_label.configure(text="¡Descarga completada!", text_color="green")

    def descargar_video(self, url, path):
        try:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self.progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.after(0, lambda: messagebox.showinfo("Éxito", "Video descargado correctamente."))
            
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)[:50]}...", text_color="red"))
            self.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error: {e}"))
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.download_btn.configure(state="normal", text="Descargar Video")

if __name__ == "__main__":
    app = App()
    app.mainloop()
