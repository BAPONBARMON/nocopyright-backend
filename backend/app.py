from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import moviepy.editor as mp

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
MODIFIED_FOLDER = 'modified'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODIFIED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return 'Backend running ✅'

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    video = request.files['video']
    path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(path)
    return jsonify({'message': 'Uploaded successfully', 'filename': video.filename})

@app.route('/modify', methods=['POST'])
def modify():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(MODIFIED_FOLDER, 'modified_' + filename)

    # Apply basic modifications: slight speed + pitch change
    clip = mp.VideoFileClip(input_path).fx(mp.vfx.speedx, 1.05)
    clip.write_videofile(output_path, audio_codec='aac', logger=None)

    return send_file(output_path, mimetype='video/mp4', as_attachment=True)
