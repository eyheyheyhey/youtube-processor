from flask import Flask, request, jsonify
import subprocess, uuid, os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    data = request.json
    job_id = str(uuid.uuid4())
    original_path = f"/tmp/{job_id}_original.mp4"
    output_path = f"/tmp/{job_id}_processed.mp4"

    # Download video
    subprocess.run([
        "yt-dlp",
        "-f", "best[height<=720]",
        "-o", original_path,
        data["videoUrl"]
    ])

    # Process with FFmpeg
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", original_path,
        "-vf", "scale=1080:1920,zoompan=z='1.2',drawtext=text='QuickDIYHacks':x=10:y=H-th-10:fontsize=24:fontcolor=white",
        "-c:v", "libx264",
        "-preset", "fast",
        output_path
    ]
    subprocess.run(ffmpeg_cmd)

    return jsonify({
        "processedUrl": f"https://your-render-url.onrender.com/download/{job_id}",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)