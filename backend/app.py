from flask import Flask, request, send_file, jsonify
import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import tempfile
import random

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def subtly_modify_audio(audio_path):
    sound = AudioSegment.from_file(audio_path)
    # Speed up audio by 2%
    sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * 1.02)
    }).set_frame_rate(sound.frame_rate)
    # Slight pitch shift by increasing frame rate temporarily
    return sound

@app.route('/')
def home():
    return jsonify({"status": "Server running"})

@app.route('/remix', methods=['POST'])
def remix_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    original_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(original_path)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            clip = VideoFileClip(original_path)

            # Extract audio
            audio_path = os.path.join(tmpdir, "original_audio.mp3")
            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

            # Modify audio
            modified_audio = subtly_modify_audio(audio_path)
            modified_audio_path = os.path.join(tmpdir, "modified_audio.mp3")
            modified_audio.export(modified_audio_path, format="mp3")

            # Apply minor visual tweak: small crop + slight brightness
            w, h = clip.size
            cropped = clip.crop(x1=2, y1=2, x2=w-2, y2=h-2)
            final_clip = cropped.set_audio(modified_audio_path).fx(lambda c: c.fl_image(lambda frame: frame * 1.02))

            # Output
            output_path = os.path.join(tmpdir, "remixed.mp4")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

            return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500