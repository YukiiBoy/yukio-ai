from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

JUICE_KEY = os.environ.get("JUICE_KEY")
API_URL = "https://api.tokenjuice.ai/v1/chat/completions"

HTML_PAGE = """
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI - V3 Fast</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>:root{--bg:#0a0a0f;--panel:#11111a;--card:#1a1a25;--border:#242436;--primary:#7c5cff;--primary2:#4a9eff;--text:#f1f1f3;--muted:#9a9ab0}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(800px at 10% -10%, rgba(124,92,255,.15), transparent), radial-gradient(800px at 90% 110%, rgba(74,158,255,.12), transparent), var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:rgba(17,17,26,.9);backdrop-filter:blur(20px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:16px;gap:12px;transition:.3s;z-index:100}
.brand{display:flex;align-items:center;gap:12px;padding:8px}.brand-logo{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800}
.btn-new{width:100%;padding:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;cursor:pointer}
#history{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:6px}.chat-item{padding:12px 14px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted);border:1px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chat-item:hover,.chat-item.active{background:var(--card);color:var(--text);border-color:var(--primary)}
#main{flex:1;display:flex;flex-direction:column;min-width:0}#topbar{padding:14px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:rgba(10,10,15,.7);backdrop-filter:blur(10px)}.hamburger{width:40px;height:40px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:none;align-items:center;justify-content:center;cursor:pointer;font-size:18px}.model-badge{padding:6px 12px;background:rgba(124,92,255,.12);border:1px solid rgba(124,92,255,.25);border-radius:20px;font-size:11px;font-weight:600;color:var(--primary)}
#chat{flex:1;overflow-y:auto;padding:24px 0}.chat-inner{max-width:780px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:24px}
.welcome{text-align:center;padding:50px 0 20px}.welcome h2{font-size:38px;font-weight:800;background:linear-gradient(135deg,#fff 30%, var(--muted));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;line-height:1.1}
.quick{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:24px auto 0;max-width:520px}.q-card{padding:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;cursor:pointer;text-align:left}.q-card:hover{border-color:var(--primary)}.q-card b{font-size:13px;display:block}.q-card span{font-size:11px;color:var(--muted)}
.msg{display:flex;gap:12px;animation:fadeIn .3s}@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}.avatar{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.7;font-size:14px;min-width:0}.bubble pre{background:#0f0f14 !important;border:1px solid var(--border);border-radius:12px;padding:14px;margin:12px 0;overflow-x:auto}
#inputArea{padding:14px 16px 20px}.input-box{max-width:780px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:6px 6px 6px 18px;display:flex;gap:10px;align-items:flex-end}.input-box:focus-within{border-color:var(--primary)}#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:22px;max-height:120px;font-family:inherit;padding:8px 0}#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:90}
@media(max-width:900px){.hamburger{display:flex}#sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#overlay.show{display:block}.welcome h2{font-size:28px}.quick{grid-template-columns:1fr}}
</style></head><body>
<div id="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar"><div class="brand"><div class="brand-logo">Y</div><div><h1>Yukio AI</h1><span style="font-size:10px;color:var(--muted)">BY YUKIOSHOP • V3 FAST</span></div></div><button class="btn-new" onclick="newChat(); if(innerWidth<=900) toggleSidebar()">+ New Chat</button><div id="history"></div><div style="padding:10px;font-size:10px;color:var(--muted);border-top:1px solid var(--border)">© 2026 Yukioshop • V3 Stable</div></div>
<div id="main"><div id="topbar"><button class="hamburger" onclick="toggleSidebar()">☰</button><div style="font-weight:700;flex:1">Chat</div><div class="model-badge">⚡ DeepSeek-V3 • Fast & Stable</div></div><div id="chat"><div class="chat-inner" id="chatInner"></div></div><div id="inputArea"><div class="input-box"><textarea id="msg" placeholder="Tanya bikin bot discord ticket, portfolio..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><button id="send" onclick="sendMsg()">↑</button></div></div></div>
<script>
let chats=JSON.parse(localStorage.getItem('yukio_v3_final')||'[]');let cur=localStorage.getItem('yukio_cur_v3')||null;
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function save(){localStorage.setItem('yukio_v3_final',JSON.stringify(chats));localStorage.setItem('yukio_cur_v3',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Chat',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC();if(innerWidth<=900)toggleSidebar()};h.appendChild(d);});}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML=`<div class=welcome><h2>Yukio AI V3<br>Super cepat.</h2><p style=color:var(--muted);font-size:13px>Tap ☰ buat history • Anti timeout</p><div class=quick>
<div class=q-card onclick="fillQ(this)"><b>🎫 Bot Ticket + Transkrip</b><span>Button & Embed</span></div>
<div class=q-card onclick="fillQ(this)"><b>🛒 Bot Toko Serbaguna</b><span>Keranjang modern</span></div>
<div class=q-card onclick="fillQ(this)"><b>🌐 Web Portfolio</b><span>Modern responsive</span></div>
<div class=q-card onclick="fillQ(this)"><b>🔧 Debug & Fix</b><span>Error jadi beres</span></div>
</div></div>`;}
function fillQ(el){document.getElementById('msg').value=el.querySelector('b').innerText;sendMsg();}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';d.innerHTML=`<div class="avatar ${m.role==='user'?'u':'y'}">${m.role==='user'?'U':'Y'}</div><div class=bubble>${m.role==='user'?escapeHtml(m.content):marked.parse(m.content)}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function autoGrow(el){el.style.height='22px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
async function sendMsg(){let i=document.getElementById('msg');let t=i.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});i.value='';autoGrow(i);renderC();save();ch.messages.push({role:'assistant',content:'<span style=color:var(--muted)>⚡ Yukio V3 lagi ngetik...</span>'});renderC();document.getElementById('send').disabled=true;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let j=await r.json();ch.messages[ch.messages.length-1].content=j.reply;}catch(e){ch.messages[ch.messages.length-1].content='Error: '+e}document.getElementById('send').disabled=false;renderC();save();}
if(!chats.length)newChat();renderH();renderC();if(chats.find(c=>c.id===cur)?.messages?.length===0)renderW();
</script></body></html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = (request.get_json(silent=True) or {}).get("message","").strip()
        if not msg:
            return jsonify({"reply": "Ketik dulu bos"})
        
        headers = {
            "Authorization": f"Bearer {JUICE_KEY}",
            "Content-Type": "application/json"
        }
        
        # === V3 PALING STABIL ANTI TIMEOUT ===
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI V3, asisten coding handal buatan Yukioshop. Jawab cepat, to the point, kasih kode lengkap pakai markdown. Kalau diminta bot ticket discord, kasih full code: ticket create dengan button, embed modern, dan transkrip pakai discord-html-transcripts. Kalau diminta web portfolio, kasih HTML+CSS+JS single file modern."},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 3000,
            "temperature": 0.7,
            "top_p": 0.9,
            "extra_body": {
                "chat_template_kwargs": {"enable_thinking": False}
            }
        }
        
        # V3 cuma butuh 8-10 detik, super cepet
        r = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        
        if r.status_code != 200:
            return jsonify({"reply": f"Error {r.status_code}: {r.text[:600]}"})
        
        data = r.json()
        message = data.get("choices", [{}])[0].get("message", {})
        reply = message.get("content") or message.get("reasoning_content") or ""
        
        if not reply.strip():
            return jsonify({"reply": "Coba lagi dengan pertanyaan lebih spesifik bos!"})
            
        return jsonify({"reply": reply.strip()})
        
    except requests.exceptions.ReadTimeout:
        return jsonify({"reply": "Timeout bos, tapi V3 harusnya gak timeout. Coba lagi!"})
    except Exception as e:
        return jsonify({"reply": f"Error V3: {e}"})
