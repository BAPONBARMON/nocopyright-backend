from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
MODIFIED_FOLDER = "modified"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODIFIED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    filename = video.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(save_path)

    return jsonify({'filename': filename}), 200

@app.route('/modify', methods=['POST'])
def modify_video():
    data = request.get_json()
    filename = data.get('filename')

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(MODIFIED_FOLDER, "modified_" + filename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        clip = VideoFileClip(input_path)

        # Copyright-safe remix: Slight speed + volume change
        modified_clip = clip.fx(lambda c: c.speedx(1.05)).volumex(1.1)

        modified_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
