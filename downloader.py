import yt_dlp
import os

def descargar_video(url, calidad, carpeta):
    opciones = {
    'format': calidad,
    'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4',
}

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

# Input del usuario
url = input("Pega el link del video: ")

print("\nElige la calidad:")
print("1 - 1080p")
print("2 - 720p")
print("3 - 480p")
print("4 - Solo audio (mp3)")

opcion = input("\nElige una opción (1-4): ")

calidades = {
    '1': 'bestvideo[height<=1080]+bestaudio/best',
    '2': 'bestvideo[height<=720]+bestaudio/best',
    '3': 'bestvideo[height<=480]+bestaudio/best',
    '4': 'bestaudio/best',
}

calidad = calidades.get(opcion, 'best')

carpeta = input("\n¿Dónde quieres guardar el video? (Enter para guardar aquí): ").strip()
if carpeta == '':
    carpeta = '.'

descargar_video(url, calidad, carpeta)