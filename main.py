import yt_dlp
import tkinter as tk
from tkinter import messagebox

def descargar_video():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Advertencia", "Pon aqui la URL de youtube")
        return

    try:
        ydl_opts = {'format': 'best'}

        # Descargar el video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Éxito", "Descarga completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

ventana = tk.Tk()
ventana.title("Descargar un video de Youtube. By: MarcausenteDev")
ventana.geometry("400x200")

url_label = tk.Label(ventana, text="Pon aqui tu URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(ventana, width=50)
url_entry.pack(pady=5)

descargar_button = tk.Button(ventana, text="Descargar Video", command=descargar_video)
descargar_button.pack(pady=20)

ventana.mainloop()
