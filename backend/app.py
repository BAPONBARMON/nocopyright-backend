from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    filename = str(uuid.uuid4()) + '_' + video.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video.save(filepath)
    return jsonify({'filename': filename}), 200

@app.route('/modify', methods=['POST'])
def modify_video():
    data = request.get_json()
    filename = data.get('filename')
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_filename = 'processed_' + filename
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)

    try:
        clip = VideoFileClip(input_path)
        modified = clip.fx(vfx.speedx, 1.05).volumex(1.1)
        modified.write_videofile(output_path, codec='libx264', audio_codec='aac')
        return jsonify({'processed_filename': output_filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_video(filename):
    path = os.path.join(PROCESSED_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)