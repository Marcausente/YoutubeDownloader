import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            p = d.get('_percent_str', '0%').replace('%', '')
            progress_var.set(float(p))
            # Force update of the GUI
            ventana.update_idletasks()
        except ValueError:
            pass
    elif d['status'] == 'finished':
        progress_var.set(100)
        messagebox.showinfo("Éxito", "Descarga completada.")
        # Reset progress bar after a short delay or immediately
        progress_var.set(0)

def confirmar_descarga():
    url = url_entry.get()
    path = folder_path.get()
    
    if not url:
        messagebox.showwarning("Advertencia", "Pon aqui la URL de youtube")
        return
        
    if not path:
        messagebox.showwarning("Advertencia", "Selecciona una carpeta de destino")
        return

    # Disable button while downloading
    descargar_button.config(state=tk.DISABLED)
    
    # Run download in a separate thread
    thread = threading.Thread(target=descargar_video, args=(url, path))
    thread.start()

def descargar_video(url, path):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
    except Exception as e:
        ventana.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error: {e}"))
    finally:
        # Re-enable button
        ventana.after(0, lambda: descargar_button.config(state=tk.NORMAL))

ventana = tk.Tk()
ventana.title("Descargar un video de Youtube. By: MarcausenteDev")
ventana.geometry("500x350")

# URL Section
url_label = tk.Label(ventana, text="Pon aqui tu URL:")
url_label.pack(pady=(20, 5))

url_entry = tk.Entry(ventana, width=60)
url_entry.pack(pady=5)

# Folder Section
folder_path = tk.StringVar()
folder_frame = tk.Frame(ventana)
folder_frame.pack(pady=10)

folder_btn = tk.Button(folder_frame, text="Seleccionar Carpeta", command=select_folder)
folder_btn.pack(side=tk.LEFT, padx=5)

folder_label = tk.Label(folder_frame, textvariable=folder_path, width=40, relief="sunken", anchor="w")
folder_label.pack(side=tk.LEFT, padx=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(ventana, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, fill=tk.X, padx=50)

# Download Button
descargar_button = tk.Button(ventana, text="Descargar Video", command=confirmar_descarga, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
descargar_button.pack(pady=10)

ventana.mainloop()
