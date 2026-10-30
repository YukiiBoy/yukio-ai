from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

JUICE_KEY = os.environ.get("JUICE_KEY")
API_URL = "https://api.tokenjuice.ai/v1/chat/completions"

HTML_PAGE = '''
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI V3</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#0a0a0f;--card:#1a1a25;--border:#242436;--primary:#7c5cff;--primary2:#4a9eff;--text:#f1f1f3;--muted:#9a9ab0}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:#11111a;border-right:1px solid var(--border);display:flex;flex-direction:column;padding:16px;gap:12px;transition:.3s;z-index:100}
.brand{display:flex;align-items:center;gap:12px;padding:8px}.brand-logo{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800}
.btn-new{width:100%;padding:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;cursor:pointer}
#history{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:6px}.chat-item{padding:12px 14px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted);border:1px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chat-item:hover,.chat-item.active{background:var(--card);color:var(--text);border-color:var(--primary)}
#main{flex:1;display:flex;flex-direction:column;min-width:0}#topbar{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px}
.hamburger{width:40px;height:40px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
.badge{padding:6px 12px;background:rgba(124,92,255,.12);border:1px solid rgba(124,92,255,.25);border-radius:20px;font-size:11px;font-weight:600;color:var(--primary)}
#chat{flex:1;overflow-y:auto;padding:24px 0}.chat-inner{max-width:780px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:24px}
.welcome{text-align:center;padding:40px 0}.welcome h2{font-size:34px;font-weight:800;margin-bottom:12px}
.quick{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:20px auto 0;max-width:520px}.q-card{padding:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;cursor:pointer;text-align:left}.q-card:hover{border-color:var(--primary)}
.msg{display:flex;gap:12px}.avatar{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.7;font-size:14px;min-width:0}.bubble pre{background:#0f0f14 !important;border:1px solid var(--border);border-radius:12px;padding:14px;margin:12px 0;overflow-x:auto}
#inputArea{padding:14px 16px 20px}.input-box{max-width:780px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:6px 6px 6px 18px;display:flex;gap:10px;align-items:flex-end}.input-box:focus-within{border-color:var(--primary)}#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:22px;max-height:120px;font-family:inherit;padding:8px 0}#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:90}
@media(max-width:900px){#sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#overlay.show{display:block}}
</style></head>
<body>
<div id="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar"><div class="brand"><div class="brand-logo">Y</div><div><b>Yukio AI</b><br><span style="font-size:10px;color:var(--muted)">BY YUKIOSHOP • V3 FAST</span></div></div><button class="btn-new" onclick="newChat(); if(window.innerWidth<=900) toggleSidebar()">+ New Chat</button><div id="history"></div></div>
<div id="main"><div id="topbar"><button class="hamburger" onclick="toggleSidebar()">☰</button><div style="font-weight:700;flex:1">Chat</div><div class="badge">⚡ DeepSeek-V3 • Fast</div></div><div id="chat"><div class="chat-inner" id="chatInner"></div></div><div id="inputArea"><div class="input-box"><textarea id="msg" placeholder="Tanya bikin bot discord ticket..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><button id="send" onclick="sendMsg()">↑</button></div></div></div>
<script>
let chats=JSON.parse(localStorage.getItem('yukio_v3')||'[]');let cur=localStorage.getItem('yukio_cur')||null;
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function save(){localStorage.setItem('yukio_v3',JSON.stringify(chats));localStorage.setItem('yukio_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Chat',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC();if(innerWidth<=900)toggleSidebar()};h.appendChild(d);});}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML='<div class=welcome><h2>Yukio AI V3<br>Super cepat.</h2><p style=color:var(--muted);font-size:13px>Tap ☰ buat history</p><div class=quick><div class=q-card onclick="fillQ(this)"><b>🎫 Bot Ticket + Transkrip</b><span>Button & Embed</span></div><div class=q-card onclick="fillQ(this)"><b>🛒 Bot Toko</b><span>Keranjang modern</span></div></div></div>';}
function fillQ(el){document.getElementById('msg').value=el.querySelector('b').innerText;sendMsg();}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';d.innerHTML='<div class="avatar '+(m.role==='user'?'u':'y')+'">'+(m.role==='user'?'U':'Y')+'</div><div class=bubble>'+(m.role==='user'?escapeHtml(m.content):marked.parse(m.content))+'</div>';inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function autoGrow(el){el.style.height='22px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
async function sendMsg(){let i=document.getElementById('msg');let t=i.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});i.value='';autoGrow(i);renderC();save();ch.messages.push({role:'assistant',content:'<span style=color:var(--muted)>⚡ V3 ngetik...</span>'});renderC();document.getElementById('send').disabled=true;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let j=await r.json();ch.messages[ch.messages.length-1].content=j.reply;}catch(e){ch.messages[ch.messages.length-1].content='Error: '+e}document.getElementById('send').disabled=false;renderC();save();}
if(!chats.length)newChat();renderH();renderC();if(chats.find(c=>c.id===cur)?.messages?.length===0)renderW();
</script></body></html>
'''

# FIX UTAMA ANTI NOT FOUND: Handle semua kemungkinan path yang di-rewrite Vercel
@app.route("/")
@app.route("/api/index")
@app.route("/api/index/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
@app.route("/api/index/chat", methods=["POST"])
@app.route("/api/chat", methods=["POST"])
def chat_api():
    try:
        data = request.get_json(silent=True) or {}
        msg = data.get("message","").strip()
        if not msg:
            return jsonify({"reply": "Ketik dulu bos"})
        headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "Kamu Yukio AI V3 by Yukioshop. Jawab cepat, kasih kode lengkap markdown."},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 3000,
            "temperature": 0.7
        }
        r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        if r.status_code != 200:
            return jsonify({"reply": f"Error {r.status_code}: {r.text[:500]}"})
        reply = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error V3: {e}"})

# Fallback untuk semua path lain -> balikin HTML biar gak Not Found
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    if path.endswith("chat") or path == "chat":
        return chat_api()
    return HTML_PAGE
