from flask import render_template, request, send_file
from main import app
import yt_dlp
import os
import tempfile

def download_audio(url):
    temp_dir = tempfile.mkdtemp(dir='/tmp')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return os.path.join(temp_dir, 'audio.mp3')
    except Exception as e:
        print(f"Erro: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/baixar', methods=['POST'])
def baixar_audio():
    url = request.form.get('url', '').strip()
    if not url:
        return "URL inválido", 400
    
    mp3_file = download_audio(url)
    if mp3_file:
        try:
            return send_file(
                mp3_file,
                as_attachment=True,
                download_name='audio.mp3'
            )
        finally:
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
                os.rmdir(os.path.dirname(mp3_file))
    return "Falha no download", 500