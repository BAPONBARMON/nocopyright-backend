from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400

    video = request.files['video']
    filename = str(uuid.uuid4()) + '.mp4'
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(input_path)

    return jsonify({'message': 'Video uploaded successfully', 'filename': filename})

@app.route('/modify', methods=['POST'])
def modify_video():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, 'modified_' + filename)

    try:
        clip = VideoFileClip(input_path)
        modified = clip.fx(vfx.speedx, 1.1).volumex(0.95)  # subtle pitch/speed change
        modified.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return jsonify({'download_url': '/download/' + 'modified_' + filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
