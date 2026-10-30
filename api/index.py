from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder='../templates')

JUICE_KEY = os.environ.get("JUICE_KEY") # Nanti key nya taro di Vercel, biar aman
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
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI, AI assistant canggih buatan Yukioshop. Jawab helpful, ramah, gaul Indonesia. Kalau ditanya coding, kasih code yang rapi."},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 1000
        }
        r = requests.post(URL, headers=headers, json=data, timeout=30)
        ai_reply = r.json()['choices'][0]['message']['content']
        return jsonify({"reply": ai_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"})

# Buat Vercel
app = app
