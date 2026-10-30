from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

JUICE_KEY = os.environ.get("JUICE_KEY")
API_URL = "https://api.tokenjuice.ai/v1/chat/completions"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI - by Yukioshop</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#0a0a0f;--panel:#11111a;--card:#1a1a25;--border:#242436;--primary:#7c5cff;--primary2:#4a9eff;--text:#f1f1f3;--muted:#9a9ab0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden;background:radial-gradient(800px at 10% -10%, rgba(124,92,255,.15), transparent), radial-gradient(800px at 90% 110%, rgba(74,158,255,.12), transparent), var(--bg)}
#sidebar{width:300px;background:rgba(17,17,26,.8);backdrop-filter:blur(20px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:16px;gap:12px}
.brand{display:flex;align-items:center;gap:12px;padding:8px}
.brand-logo{width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:18px;box-shadow:0 4px 20px rgba(124,92,255,.4)}
.brand h1{font-size:18px;font-weight:700}.brand span{font-size:11px;color:var(--muted);letter-spacing:.5px}
.btn-new{width:100%;padding:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;font-size:14px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(124,92,255,.3);transition:.2s}
.btn-new:hover{transform:translateY(-1px);box-shadow:0 6px 28px rgba(124,92,255,.4)}
#history{flex:1;overflow-y:auto;margin-top:8px;display:flex;flex-direction:column;gap:6px}
.chat-item{padding:12px 14px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted);border:1px solid transparent;transition:.15s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chat-item:hover{background:var(--card);color:var(--text);border-color:var(--border)}
.chat-item.active{background:var(--card);color:var(--text);border-color:var(--primary);box-shadow:0 0 0 1px rgba(124,92,255,.2)}
#main{flex:1;display:flex;flex-direction:column;position:relative}
#topbar{padding:18px 24px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;background:rgba(10,10,15,.6);backdrop-filter:blur(10px)}
.model-badge{padding:6px 12px;background:rgba(124,92,255,.12);border:1px solid rgba(124,92,255,.25);border-radius:20px;font-size:12px;font-weight:600;color:var(--primary)}
#chat{flex:1;overflow-y:auto;padding:32px 0}
.chat-inner{max-width:780px;margin:0 auto;padding:0 24px;display:flex;flex-direction:column;gap:28px}
.welcome{text-align:center;padding:60px 0 20px}
.welcome h2{font-size:42px;font-weight:800;line-height:1.1;background:linear-gradient(135deg,#fff 30%, var(--muted));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}
.welcome p{color:var(--muted);font-size:15px}
.quick{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:28px auto 0;max-width:520px}
.q-card{padding:16px;background:var(--card);border:1px solid var(--border);border-radius:16px;cursor:pointer;transition:.2s;text-align:left}
.q-card:hover{border-color:var(--primary);transform:translateY(-2px)}
.q-card b{font-size:13px;display:block;margin-bottom:4px}.q-card span{font-size:12px;color:var(--muted)}
.msg{display:flex;gap:16px;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.avatar{width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;flex-shrink:0}
.u{background:#fff;color:#000;box-shadow:0 2px 10px rgba(255,255,255,.15)}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;box-shadow:0 4px 15px rgba(124,92,255,.3)}
.bubble{flex:1;line-height:1.7;font-size:14.5px;min-width:0}
.bubble p{margin:8px 0}
.bubble pre{background:#0f0f14 !important;border:1px solid var(--border);border-radius:14px;padding:16px;margin:14px 0;overflow-x:auto;position:relative}
.bubble code{font-family:'JetBrains Mono',monospace;font-size:13px}
#inputArea{padding:16px 24px 24px;background:linear-gradient(to top, var(--bg) 60%, transparent)}
.input-box{max-width:780px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:8px 8px 8px 20px;display:flex;align-items:flex-end;gap:10px;box-shadow:0 10px 40px rgba(0,0,0,.4),0 0 0 1px rgba(255,255,255,.03) inset;transition:.2s}
.input-box:focus-within{border-color:var(--primary);box-shadow:0 10px 40px rgba(0,0,0,.5),0 0 0 1px var(--primary)}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:15px;resize:none;max-height:120px;min-height:24px;padding:10px 0;font-family:inherit}
#send{width:40px;height:40px;border-radius:14px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0}
#send:hover{transform:scale(1.05)}#send:disabled{opacity:.4;cursor:not-allowed}
@media(max-width:800px){#sidebar{display:none}#chat{padding:16px 0}.welcome h2{font-size:32px}.quick{grid-template-columns:1fr}}
</style>
</head>
<body>
<div id="sidebar">
  <div class="brand"><div class="brand-logo">Y</div><div><h1>Yukio AI</h1><span>BY YUKIOSHOP • V4.1 FLASH</span></div></div>
  <button class="btn-new" onclick="newChat()"><span>+</span> New Chat</button>
  <div id="history"></div>
  <div style="padding:12px;font-size:11px;color:var(--muted);border-top:1px solid var(--border)">© 2026 Yukioshop<br>Model: V4.1-Flash-1017</div>
</div>
<div id="main">
  <div id="topbar"><div style="font-weight:700">Chat</div><div class="model-badge">⚡ DeepSeek-V4.1-Flash-1017 • Active</div></div>
  <div id="chat"><div class="chat-inner" id="chatInner"></div></div>
  <div id="inputArea"><div class="input-box"><textarea id="msg" placeholder="Tanya bikin bot discord, embed, button..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><button id="send" onclick="sendMsg()"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg></button></div><div style="text-align:center;font-size:11px;color:var(--muted);margin-top:10px">Yukio AI V4.1 Flash bisa salah, cek lagi code nya ya bos!</div></div>
</div>
<script>
let chats=JSON.parse(localStorage.getItem('yukio_v41_final')||'[]');let cur=localStorage.getItem('yukio_cur_v41_final')||null;
function save(){localStorage.setItem('yukio_v41_final',JSON.stringify(chats));localStorage.setItem('yukio_cur_v41_final',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Chat',messages:[]});save();renderC();renderW();document.getElementById('msg').focus();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC()};h.appendChild(d);});}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML=`<div class=welcome><h2>Yukio AI<br>buatin bot impian lu.</h2><p>Bot toko serbaguna, embed modern, button keren. Tanya aja bos!</p><div class=quick>
<div class=q-card onclick="fillQ(this)"><b>🛒 Bot Toko Serbaguna</b><span>Embed + Button + Keranjang</span></div>
<div class=q-card onclick="fillQ(this)"><b>🎨 Embed Modern</b><span>Design keren kaya brand besar</span></div>
<div class=q-card onclick="fillQ(this)"><b>⚙️ Slash Commands</b><span>Setup lengkap discord.js v14</span></div>
<div class=q-card onclick="fillQ(this)"><b>💳 Payment System</b><span>Integrasi midtrans & QRIS</span></div>
</div></div>`;}
function fillQ(el){document.getElementById('msg').value=el.querySelector('b').innerText;sendMsg();}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';let av=m.role==='user'?'U':'Y';let cl=m.role==='user'?'u':'y';d.innerHTML=`<div class="avatar ${cl}">${av}</div><div class=bubble>${m.role==='user'?escapeHtml(m.content):marked.parse(m.content)}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function autoGrow(el){el.style.height='24px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
async function sendMsg(){let i=document.getElementById('msg');let t=i.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});i.value='';autoGrow(i);renderC();save();ch.messages.push({role:'assistant',content:'<span style=color:var(--muted)>⚡ Yukio V4.1 Flash lagi ngetik...</span>'});renderC();document.getElementById('send').disabled=true;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let j=await r.json();ch.messages[ch.messages.length-1].content=j.reply;}catch(e){ch.messages[ch.messages.length-1].content='Error: '+e}document.getElementById('send').disabled=false;renderC();save();}
if(!chats.length)newChat();renderH();renderC();
if(chats.find(c=>c.id===cur)?.messages?.length===0)renderW();
</script>
</body>
</html>
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
        
        # === MODEL V4.1 FLASH YANG LU MAU BOS ===
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI V4.1 Flash, asisten coding handal buatan Yukioshop. Jawab langsung to the point, kasih kode lengkap dengan markdown. Jangan bertele-tele."},
                {"role": "user", "content": msg}
            ],
            "max_tokens": 2500,
            "temperature": 0.7,
            "top_p": 0.85,
            "stream": False
        }
        
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if r.status_code != 200:
            return jsonify({"reply": f"Error TokenJuice {r.status_code}: {r.text[:600]}"})
        
        data = r.json()
        message = data.get("choices", [{}])[0].get("message", {})
        
        # V4.1 Flash kadang jawab di reasoning_content
        reply = message.get("content") or message.get("reasoning_content") or ""
        
        if not reply.strip():
            reply = "Waduh jawaban kosong bos, coba tanya lebih pendek: misal 'bikin embed toko discord.js v14'"
        
        return jsonify({"reply": reply.strip()})
        
    except requests.exceptions.ReadTimeout:
        return jsonify({"reply": "⏱️ V4.1 Flash timeout 30 detik, model lagi overload bos. Coba lagi ya!"})
    except Exception as e:
        return jsonify({"reply": f"Error V4.1: {e}"})
