# 🎬 Youtify Video Downloader 🚀

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen)
![yt-dlp](https://img.shields.io/badge/Powered_by-yt--dlp-red)

Una aplicación de escritorio moderna y ligera para descargar videos y playlists completas de YouTube en formato MP4 y máxima calidad. Construida en Python con una interfaz gráfica intuitiva (CustomTkinter) y un sistema automatizado para el manejo de dependencias.

## ✨ Características Principales

* **🖥️ Interfaz Gráfica Moderna:** UI limpia, atractiva y adaptable al modo del sistema.
* **⚙️ Autogestión de FFmpeg:** La aplicación descarga y configura automáticamente `FFmpeg` y `FFprobe` en segundo plano para fusionar video y audio sin intervenciones manuales.
* **📂 Portabilidad Total:** Crea de forma automática y aislada la carpeta `descargas_videos` justo al lado del ejecutable o script.
* **🧹 Limpieza Automática:** Elimina los ejecutables temporales de conversión al terminar la descarga, manteniendo el entorno impecable.
* **🛡️ Bypass de Seguridad (PoW):** Preparado para integrar Node.js y evitar restricciones de JavaScript en YouTube.

---

## 🛠️ Requisitos Previos

Antes de ejecutar o compilar el código fuente, prepara tu entorno:

### 1. Instalar Node.js (Requerido para evitar restricciones de YouTube)
1. Descarga la versión LTS desde [nodejs.org](https://nodejs.org/).
2. Instálalo asegurándote de agregarlo al PATH del sistema.
3. Reinicia tu terminal después de la instalación.

### 2. Actualizar PIP y yt-dlp
Abre tu terminal y ejecuta:
```bash
python -m pip install --upgrade pip
python -m pip install --upgrade yt-dlp
