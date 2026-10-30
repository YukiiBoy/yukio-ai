from flask import Flask, request, jsonify, render_template
import requests
import os

# Fix path biar Vercel nemu templates
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

JUICE_KEY = os.environ.get("JUICE_KEY")
URL = "https://api.tokenjuice.ai/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message")
        headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI buatan Yukioshop, ramah dan gaul Indonesia."},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 1000
        }
        r = requests.post(URL, headers=headers, json=data, timeout=30)
        j = r.json()
        ai_reply = j['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"Error bos: {e}"})

# WAJIB BUAT VERCEL
app = app
