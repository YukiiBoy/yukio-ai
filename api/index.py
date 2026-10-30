from flask import Flask, request, jsonify, render_template
import os, requests

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

JUICE_KEY = os.environ.get("JUICE_KEY")
URL = "https://api.tokenjuice.ai/v1/chat/completions"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message", "")
        headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI buatan Yukioshop."},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 1000
        }
        r = requests.post(URL, headers=headers, json=payload, timeout=30)
        reply = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {e} | cek JUICE_KEY di Vercel"})

# Penting buat Vercel
if __name__ == "__main__":
    app.run()
