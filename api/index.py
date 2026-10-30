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
        data = request.get_json()
        user_msg = data.get("message","") if data else ""
        if not user_msg.strip():
            return jsonify({"reply": "Ketik pesan dulu bos!"})

        headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI, asisten coding handal buatan Yukioshop. Jawab dengan jelas, kasih kode lengkap kalau diminta. Gunakan markdown untuk kode."},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        r = requests.post(URL, headers=headers, json=payload, timeout=60)
        
        # DEBUG: kalau error dari TokenJuice
        if r.status_code != 200:
            return jsonify({"reply": f"Error API TokenJuice ({r.status_code}): {r.text[:500]}"})

        j = r.json()
        if "choices" not in j or not j["choices"]:
            return jsonify({"reply": f"Error format API: {str(j)[:500]}"})

        reply = j["choices"][0]["message"]["content"]
        if not reply:
            reply = "Waduh jawaban kosong dari AI, coba tanya lagi bos!"

        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"reply": f"Error server: {str(e)}"})

# Vercel butuh ini
app = app
