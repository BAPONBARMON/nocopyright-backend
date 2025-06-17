from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from moviepy.editor import VideoFileClip
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    filename = str(uuid.uuid4()) + "_" + video_file.filename
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    video_file.save(video_path)

    return jsonify({'message': 'Video uploaded successfully', 'filename': filename})

@app.route('/modify', methods=['POST'])
def modify_video():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"modified_{filename}")

    try:
        clip = VideoFileClip(input_path)
        # Subtle copyright-safe edit
        clip = clip.volumex(1.1).fx(lambda c: c.speedx(1.02))  # audio pitch & speed
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Video modified successfully', 'download_url': f"/download/{os.path.basename(output_path)}"})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
