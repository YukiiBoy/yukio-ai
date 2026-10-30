from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

# GITHUB AI - CUKUP PAKAI TOKEN GITHUB!
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") # isi ghp_xxx di Vercel
API_URL = "https://models.github.ai/inference/chat/completions"

HTML_PAGE = '''
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI • GitHub Models</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#07070b;--card:#171723;--border:#242436;--primary:#8b5cf6;--primary2:#3b82f6;--text:#f5f5f7;--muted:#9a9ab8}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:#11111a;border-right:1px solid var(--border);display:flex;flex-direction:column;padding:14px;gap:12px;transition:.3s;z-index:100}
#main{flex:1;display:flex;flex-direction:column;min-width:0}#topbar{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px}
.hamburger{width:40px;height:40px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:flex;align-items:center;justify-content:center;cursor:pointer}
#chat{flex:1;overflow-y:auto;padding:20px 0}.chat-inner{max-width:800px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:24px}
.msg{display:flex;gap:12px}.avatar{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-weight:800}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.7;font-size:14px}.bubble pre{background:#0e0e17 !important;border:1px solid var(--border);border-radius:12px;padding:14px;margin:12px 0;overflow-x:auto;position:relative}
#inputArea{padding:12px 16px 18px}.input-wrap{max-width:800px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:8px 8px 8px 16px;display:flex;gap:8px;align-items:flex-end}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;font-family:inherit;padding:8px 0}
#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer}
</style></head>
<body>
<div id="sidebar"><div style="padding:8px;font-weight:800">Yukio AI • GitHub</div><button onclick="newChat()" style="width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:12px;color:#fff;font-weight:700;cursor:pointer">+ New Chat</button><div id="history" style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px"></div></div>
<div id="main"><div id="topbar"><button class="hamburger" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button><div style="font-weight:700;flex:1">GitHub Models • Free</div><div style="padding:6px 12px;background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.3);border-radius:20px;font-size:11px">⚡ DeepSeek-V3 via GitHub</div></div><div id="chat"><div class="chat-inner" id="chatInner"></div></div><div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Tanya... pakai GitHub AI gratis!" rows="1" oninput="this.style.height='24px';this.style.height=this.scrollHeight+'px'" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendMsg()}"></textarea><button id="send" onclick="sendMsg()">↑</button></div></div></div>
<script>
let chats=JSON.parse(localStorage.getItem('yukio_github')||'[]');let cur=localStorage.getItem('yukio_github_cur')||null;
function save(){localStorage.setItem('yukio_github',JSON.stringify(chats));localStorage.setItem('yukio_github_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Chat',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.style.cssText='padding:10px 12px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted)';d.className=c.id===cur?'active':'';if(c.id===cur)d.style.cssText+=';background:var(--card);color:var(--text)';d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC()};h.appendChild(d);})}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){inner.innerHTML='<div style="text-align:center;padding:40px"><h1 style="font-size:32px;font-weight:800">Yukio AI via GitHub</h1><p style="color:var(--muted);margin-top:8px">Gratis pakai GitHub Models • DeepSeek-V3</p></div>';return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';d.innerHTML=`<div class="avatar ${m.role==='user'?'u':'y'}">${m.role==='user'?'U':'Y'}</div><div class=bubble>${m.role==='user'?m.content.replace(/</g,'&lt;'):marked.parse(m.content)}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
async function sendMsg(){let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});input.value='';renderC();save();ch.messages.push({role:'assistant',content:'⚡ GitHub AI ngetik...'});renderC();try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let j=await r.json();ch.messages[ch.messages.length-1].content=j.reply;}catch(e){ch.messages[ch.messages.length-1].content='Error: '+e}renderC();save();}
if(!chats.length)newChat();renderH();renderC();
</script></body></html>
'''

@app.route("/", methods=["GET","POST"])
@app.route("/api/index", methods=["GET","POST"])
def main_route():
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            msg = data.get("message","").strip()
            if not msg:
                return jsonify({"reply":"Ketik dulu bos!"})
            if not GITHUB_TOKEN:
                return jsonify({"reply":"⚠️ GITHUB_TOKEN belum di-set di Vercel! Buat token di github.com/settings/tokens"})
            
            headers = {
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/json"
            }
            # PILIH MODEL GITHUB - BISA GANTI-GANTI GRATIS!
            # Pilihan: gpt-4o-mini, gpt-4o, DeepSeek-V3-0324, DeepSeek-R1, Llama-3.3-70B-Instruct, Phi-4
            payload = {
                "model": "DeepSeek-V3-0324",  # <- GANTI MODEL DISINI SESUKA LU!
                "messages": [
                    {"role": "system", "content": "Kamu Yukio AI by Yukioshop via GitHub Models. Expert coding Discord bot v14, web modern."},
                    {"role": "user", "content": msg}
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
            r = requests.post(API_URL, headers=headers, json=payload, timeout=25)
            if r.status_code != 200:
                return jsonify({"reply": f"Error GitHub {r.status_code}: {r.text[:600]}"})
            reply = r.json()["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"reply": f"Error GitHub AI: {e}"})
    else:
        return HTML_PAGE

@app.route("/<path:path>", methods=["GET","POST"])
def catch_all(path):
    return main_route()
