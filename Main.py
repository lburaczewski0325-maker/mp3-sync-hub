import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    output_filename = f"output_{os.urandom(4).hex()}.mp3"
    
    # yt-dlp command to extract audio and encode to high quality MP3 (handles playlists too)
    command = [
        'yt-dlp',
        '-x', '--audio-format', 'mp3', '--audio-quality', '0',
        '-o', output_filename.replace('.mp3', '.%(ext)s'),
        url
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if not os.path.exists(output_filename):
            files = [f for f in os.listdir('.') if f.startswith(output_filename.split('_')[0])]
            if files:
                output_filename = files[0]

        return send_file(output_filename, as_attachment=True, mimetype='audio/mp3')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
