import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import urllib.request
import zipfile
from yt_dlp import YoutubeDL

# Configuración inicial de la apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def asegurar_ffmpeg():
    ffmpeg_exe = "ffmpeg.exe"
    if os.path.exists(ffmpeg_exe):
        return
    
    print("[*] Descargando componentes de conversión (FFmpeg)...")
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = "ffmpeg_temp.zip"
    
    try:
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("bin/ffmpeg.exe") or file.endswith("bin/ffprobe.exe"):
                    filename = os.path.basename(file)
                    with zip_ref.open(file) as source, open(filename, "wb") as target:
                        target.write(source.read())
    except Exception as e:
        print(f"[✘] Error con FFmpeg: {e}")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

class YoutifyVideoApp(ctk.CTk):
  def __init__(self):
    super().__init__()

    self.title("Youtify - Descargador de Videos MP4")
    self.geometry("600x420")
    self.resizable(False, False)

    # Detecta si es un .exe compilado o un script para portabilidad total
    if getattr(sys, 'frozen', False):
        self.directorio_actual = os.path.dirname(sys.executable)
    else:
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Carpeta específica para videos
    self.ruta_destino = os.path.join(self.directorio_actual, "descargas_videos")
    os.makedirs(self.ruta_destino, exist_ok=True)

    # --- INTERFAZ ---
    self.titulo_label = ctk.CTkLabel(
        self, text="Youtify - Descargador de Videos MP4", font=("Arial", 20, "bold")
    )
    self.titulo_label.pack(pady=20)

    self.url_label = ctk.CTkLabel(
        self, text="Pega el enlace del Video o Playlist:", font=("Arial", 12)
    )
    self.url_label.pack(anchor="w", padx=40)

    self.url_entry = ctk.CTkEntry(
        self,
        placeholder_text="https://www.youtube.com/watch?v=...",
        width=520,
        height=35,
    )
    self.url_entry.pack(pady=5)

    self.carpeta_label = ctk.CTkLabel(
        self,
        text=f"Tus videos se guardarán en:\n{self.ruta_destino}",
        font=("Arial", 11),
        text_color="gray",
        justify="center"
    )
    self.carpeta_label.pack(pady=15)

    self.btn_descargar = ctk.CTkButton(
        self,
        text="Descargar en MP4",
        font=("Arial", 14, "bold"),
        fg_color="#007bff",
        hover_color="#0056b3",
        width=250,
        height=40,
        command=self.iniciar_hilo_descarga,
    )
    self.btn_descargar.pack(pady=10)

    self.estado_textbox = ctk.CTkTextbox(self, width=520, height=120)
    self.estado_textbox.pack(pady=10)
    self.estado_textbox.insert("0.1", "Listo para descargar videos...\n")
    self.estado_textbox.configure(state="disabled")

  def log(self, mensaje):
    self.estado_textbox.configure(state="normal")
    self.estado_textbox.insert("end", mensaje + "\n")
    self.estado_textbox.see("end")
    self.estado_textbox.configure(state="disabled")

  def iniciar_hilo_descarga(self):
    url = self.url_entry.get().strip()
    if not url:
      messagebox.showerror("Error", "Por favor, ingresa un enlace.")
      return

    self.btn_descargar.configure(state="disabled", text="Descargando...")
    hilo = threading.Thread(target=self.ejecutar_descarga, args=(url,))
    hilo.start()

  def ejecutar_descarga(self, url):
    os.chdir(self.directorio_actual)
    asegurar_ffmpeg()
    
    os.makedirs(self.ruta_destino, exist_ok=True)

    # Configuración de yt-dlp para unir video HD y audio en MP4
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": "%(title)s.%(ext)s", 
        "progress_hooks": [self.hook_progreso],
        "windowsfilenames": True,
        "restrictfilenames": True, 
        "ffmpeg_location": self.directorio_actual,
    }

    try:
      self.log(f"\n[+] Iniciando proceso en:\n{self.ruta_destino}")
      os.chdir(self.ruta_destino)
      
      with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
      self.log("[✔] ¡Todas las descargas finalizaron con éxito en MP4!")
      messagebox.showinfo("Completado", "¡Revisa tu nueva carpeta 'descargas_videos'!")
      
    except Exception as e:
      self.log(f"[✘] Error crítico: {e}")
      messagebox.showerror("Error", f"Ocurrió un error: {e}")
      
    finally:
      os.chdir(self.directorio_actual)
      
      self.log("[*] Limpiando archivos temporales...")
      for exe in ["ffmpeg.exe", "ffprobe.exe"]:
          ruta_exe = os.path.join(self.directorio_actual, exe)
          if os.path.exists(ruta_exe):
              try:
                  os.remove(ruta_exe)
              except Exception:
                  pass
                  
      self.btn_descargar.configure(state="normal", text="Descargar en MP4")

  def hook_progreso(self, d):
    if d["status"] == "downloading":
      porcentaje = d.get("_percent_str", "0%")
      velocidad = d.get("_speed_str", "0B/s")
      self.log(f"Descargando: {porcentaje.strip()} - Velocidad: {velocidad.strip()}")
    elif d["status"] == "finished":
      self.log("[*] Descarga finalizada, uniendo video y audio en MP4...")

if __name__ == "__main__":
  app = YoutifyVideoApp()
  app.mainloop()