from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def info():
    data = request.json
    url = data.get('url')
    
    opciones = {'quiet': True}
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        resultado = ydl.extract_info(url, download=False)
        
        if resultado.get('_type') == 'playlist':
            return jsonify({'error': 'Es una playlist, pega el link de un video individual'}), 400
        
        return jsonify({
            'titulo': resultado.get('title'),
            'miniatura': resultado.get('thumbnail'),
            'duracion': resultado.get('duration_string', ''),
            'canal': resultado.get('uploader')
        })

@app.route('/descargar', methods=['POST'])
def descargar():
    data = request.json
    url = data.get('url')
    calidad = data.get('calidad', 'best')

    calidades = {
        '1': 'bestvideo[height<=1080]+bestaudio/best',
        '2': 'bestvideo[height<=720]+bestaudio/best',
        '3': 'bestvideo[height<=480]+bestaudio/best',
        '4': 'bestaudio/best',
    }

    calidad_seleccionada = calidades.get(calidad, 'best')
    carpeta_temp = tempfile.mkdtemp()

    opciones = {
        'format': calidad_seleccionada,
        'outtmpl': os.path.join(carpeta_temp, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

    archivo = os.listdir(carpeta_temp)[0]
    ruta = os.path.join(carpeta_temp, archivo)

    return send_file(ruta, as_attachment=True, download_name=archivo)

if __name__ == '__main__':
    app.run(debug=True)