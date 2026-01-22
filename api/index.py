from flask import Flask, request, jsonify, render_template_string
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# মূল এপিআই এন্ডপয়েন্ট
TARGET_API = "https://ytdl.socialplug.io/api/video-info"

@app.route('/')
def home():
    return render_template_string(open('index.html').read())

@app.route('/api/fetch', methods=['GET'])
def fetch_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL is required", "developer": "Saiful Islam"}), 400

    try:
        # সোশ্যাল-প্লাগ এপিআই কল করা
        response = requests.get(f"{TARGET_API}?url={video_url}")
        data = response.json()
        
        # আপনার ব্র্যান্ডিং ডাটা যুক্ত করা
        data["developer"] = "Saiful Islam"
        data["contact"] = "saifulsajedul@gmail.com"
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e), "developer": "Saiful Islam"}), 500

if __name__ == '__main__':
    app.run()
