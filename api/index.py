from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import yt_dlp
import os
import shutil

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template_string(open('index.html').read())

@app.route('/api/video-info', methods=['GET'])
def get_video_info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL is required", "developer": "Saiful Islam"}), 400

    cookie_src = os.path.join(os.path.dirname(__file__), '..', 'cookies.txt')
    cookie_dest = '/tmp/cookies.txt'

    try:
        if os.path.exists(cookie_src):
            shutil.copy2(cookie_src, cookie_dest)

        ydl_opts = {
            'quiet': True,
            'cookiefile': cookie_dest if os.path.exists(cookie_dest) else None,
            'format': 'best',
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            formats = []
            for f in info.get('formats', []):
                # ভিডিও এবং অডিও আছে এমন লিঙ্কগুলো ফিল্টার করা
                if f.get('url') and f.get('vcodec') != 'none':
                    quality = f.get('format_note') or f"{f.get('height')}p"
                    formats.append({
                        "quality": quality,
                        "url": f.get('url'),
                        "ext": f.get('ext'),
                        "size": f.get('filesize') or f.get('filesize_approx')
                    })

            # ডুপ্লিকেট কোয়ালিটি বাদ দিয়ে সুন্দর লিস্ট তৈরি করা
            seen_quality = set()
            final_formats = []
            for fmt in formats:
                if fmt['quality'] not in seen_quality:
                    final_formats.append(fmt)
                    seen_quality.add(fmt['quality'])

            return jsonify({
                "success": True,
                "developer": "Saiful Islam",
                "contact": "saifulsajedul@gmail.com",
                "title": info.get('title'),
                "image": info.get('thumbnail'),
                "duration": info.get('duration'),
                "formats": final_formats
            }), 200

    except Exception as e:
        return jsonify({"error": str(e), "developer": "Saiful Islam"}), 500

app = app

