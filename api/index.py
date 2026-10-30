from flask import Flask, request, jsonify
import os, requests, time
app = Flask(__name__)

JUICE_KEY = os.environ.get("JUICE_KEY")
API_URL = "https://api.tokenjuice.ai/v1/chat/completions"

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI V4 • Aurora</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#07070b;--bg2:#0f0f18;--card:#171723;--card2:#1e1e2e;--border:#242436;--border2:#2e2e45;--primary:#8b5cf6;--primary2:#3b82f6;--text:#f5f5f7;--muted:#9a9ab8;--success:#22c55e}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(1200px 600px at 20% -10%, rgba(139,92,246,.15), transparent), radial-gradient(800px 400px at 80% 0%, rgba(59,130,246,.12), transparent), var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:320px;background:rgba(17,17,26,.9);backdrop-filter:blur(20px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:14px;gap:12px;transition:.3s;z-index:100}
.brand{display:flex;align-items:center;gap:12px;padding:10px 8px}
.logo{width:42px;height:42px;border-radius:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 8px 24px rgba(139,92,246,.3)}
.search{position:relative}.search input{width:100%;padding:10px 12px 10px 36px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--text);outline:none;font-size:13px}.search span{position:absolute;left:12px;top:11px;opacity:.6}
.btn-new{width:100%;padding:13px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 8px 20px rgba(139,92,246,.3)}
.btn-new:hover{transform:translateY(-1px)}
#history{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px;margin-top:4px}
.group-label{font-size:10px;font-weight:700;letter-spacing:.1em;color:var(--muted);padding:10px 8px 4px}
.chat-item{padding:11px 12px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted);border:1px solid transparent;display:flex;align-items:center;justify-content:space-between;gap:8px}
.chat-item:hover{background:var(--card);color:var(--text);border-color:var(--border2)}.chat-item.active{background:var(--card2);color:var(--text);border-color:var(--primary);box-shadow:0 0 0 1px rgba(139,92,246,.2) inset}
.chat-item .dots{opacity:0}.chat-item:hover .dots{opacity:1}
.bottom{border-top:1px solid var(--border);padding-top:10px;display:flex;flex-direction:column;gap:6px}
.btn-ghost{width:100%;padding:10px 12px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--muted);font-size:12px;cursor:pointer;text-align:left;display:flex;gap:8px;align-items:center}.btn-ghost:hover{color:var(--text);border-color:var(--border2)}
#main{flex:1;display:flex;flex-direction:column;min-width:0}
#topbar{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:rgba(15,15,24,.6);backdrop-filter:blur(12px)}
.hamburger{width:40px;height:40px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px}
.model-pill{padding:7px 12px;background:linear-gradient(135deg,rgba(139,92,246,.15),rgba(59,130,246,.15));border:1px solid rgba(139,92,246,.3);border-radius:20px;font-size:11px;font-weight:700;display:flex;gap:6px;align-items:center}
#chat{flex:1;overflow-y:auto;padding:20px 0;scroll-behavior:smooth}
.chat-inner{max-width:800px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:28px}
.welcome{text-align:center;padding:30px 0 10px}.welcome h1{font-size:38px;font-weight:800;letter-spacing:-.02em;background:linear-gradient(135deg,#fff 30%,#a78bfa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.welcome p{color:var(--muted);font-size:14px;margin-top:10px}
.prompts{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:24px auto 0;max-width:640px}
.p-card{padding:16px;background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--border);border-radius:16px;cursor:pointer;text-align:left;transition:.2s}.p-card:hover{border-color:var(--primary);transform:translateY(-2px);box-shadow:0 12px 32px rgba(0,0,0,.3)}.p-card b{font-size:13px;display:block;margin-bottom:4px}.p-card span{font-size:11px;color:var(--muted);line-height:1.4;display:block}
.msg{display:flex;gap:14px;animation:fade .3s ease}.avatar{width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0;box-shadow:0 4px 12px rgba(0,0,0,.2)}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.75;font-size:14.5px;min-width:0}.bubble a{color:#a78bfa}
.bubble pre{position:relative;background:#0e0e17 !important;border:1px solid var(--border);border-radius:14px;padding:14px;margin:14px 0;overflow-x:auto}
.copy-btn{position:absolute;right:8px;top:8px;padding:6px 10px;background:var(--card2);border:1px solid var(--border);border-radius:8px;font-size:11px;color:var(--muted);cursor:pointer}
.actions{display:flex;gap:8px;margin-top:10px}.act{padding:6px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer}.act:hover{color:var(--text);border-color:var(--border2)}
#inputArea{padding:12px 16px 18px;background:linear-gradient(0deg,var(--bg) 30%, transparent)}
.input-wrap{max-width:800px;margin:0 auto;background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:8px 8px 8px 16px;display:flex;gap:8px;align-items:flex-end;box-shadow:0 12px 40px rgba(0,0,0,.4), 0 0 0 1px rgba(255,255,255,.02) inset;transition:.2s}
.input-wrap:focus-within{border-color:var(--primary);box-shadow:0 12px 40px rgba(0,0,0,.4), 0 0 0 1px rgba(139,92,246,.3) inset}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;max-height:140px;font-family:inherit;padding:8px 0;line-height:1.6}
.tools{display:flex;gap:6px;align-items:center}
.icon-btn{width:36px;height:36px;border-radius:11px;border:1px solid var(--border);background:var(--card2);color:var(--muted);cursor:pointer;display:flex;align-items:center;justify-content:center}
#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer;font-weight:700;box-shadow:0 6px 16px rgba(139,92,246,.4)}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);backdrop-filter:blur(2px);z-index:90}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:900px){#sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#overlay.show{display:block}.prompts{grid-template-columns:1fr}.welcome h1{font-size:30px}}
</style></head>
<body>
<div id="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar">
<div class="brand"><div class="logo">Y</div><div><b>Yukio AI</b><div style="font-size:10px;color:var(--muted);letter-spacing:.08em">AURORA V4 • YUKIOSHOP</div></div></div>
<button class="btn-new" onclick="newChat()">✦ New Chat</button>
<div class="search"><span>🔍</span><input id="search" placeholder="Cari chat..." oninput="filterChats()"></div>
<div id="history"></div>
<div class="bottom">
<button class="btn-ghost" onclick="exportChats()">📤 Export Chat (MD)</button>
<button class="btn-ghost" onclick="clearAll()">🗑️ Hapus Semua</button>
<div style="font-size:10px;color:var(--muted);text-align:center;padding-top:4px">DeepSeek-V3 • TokenJuice • 2026 Yukioshop</div>
</div>
</div>
<div id="main">
<div id="topbar"><button class="hamburger" onclick="toggleSidebar()">☰</button><div style="font-weight:700;flex:1">Chat</div><div class="model-pill">⚡ DeepSeek-V3 • Fast</div><button class="icon-btn" onclick="toggleTheme()" title="Theme">◐</button></div>
<div id="chat"><div class="chat-inner" id="chatInner"></div></div>
<div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Tanya apa aja... misal: bikin bot Discord ticket + transkrip..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><div class="tools"><button class="icon-btn" onclick="startVoice()" title="Voice">🎤</button><button id="send" onclick="sendMsg()">↑</button></div></div><div style="max-width:800px;margin:8px auto 0;text-align:center;font-size:10px;color:var(--muted)">Yukio bisa bikin kesalahan. Cek kode penting sebelum deploy.</div></div>
</div>
<script>
marked.setOptions({gfm:true,breaks:true});
let chats=JSON.parse(localStorage.getItem('yukio_v4')||'[]');let cur=localStorage.getItem('yukio_cur_v4')||null;
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function save(){localStorage.setItem('yukio_v4',JSON.stringify(chats));localStorage.setItem('yukio_cur_v4',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Chat',created:Date.now(),messages:[]});save();renderC();}
function filterChats(){renderH(document.getElementById('search').value.toLowerCase())}
function renderH(q=''){let h=document.getElementById('history');h.innerHTML='';let f=chats.filter(c=>c.title.toLowerCase().includes(q));let today=[];f.forEach(c=>today.push(c));if(today.length){let l=document.createElement('div');l.className='group-label';l.textContent='TODAY';h.appendChild(l);today.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.innerHTML='<span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+esc(c.title)+'</span><span class=dots>⋯</span>';d.onclick=()=>{cur=c.id;save();renderC();if(innerWidth<=900)toggleSidebar()};let dot=d.querySelector('.dots');dot.onclick=(e)=>{e.stopPropagation();if(confirm('Hapus chat ini?')){chats=chats.filter(x=>x.id!==c.id);save();if(cur===c.id){cur=chats[0]?.id||null;renderC()}}};h.appendChild(d);})}}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML=`<div class=welcome><h1>Apa yang mau kamu buat hari ini?</h1><p>Yukio V4 Aurora • Cepat, clean, dan paham coding Discord, web, bot</p><div class=prompts><div class=p-card onclick="useP('Bikinin bot Discord ticket dengan button, embed, dan transkrip HTML otomatis')"><b>🎫 Bot Ticket Pro</b><span>Button, embed, transcript HTML, log channel</span></div><div class=p-card onclick="useP('Bikin web portfolio modern dark glassmorphism untuk Yukioshop')"><b>🌌 Portfolio Aurora</b><span>Glassmorphism, animasi, responsive</span></div><div class=p-card onclick="useP('Bikin bot Discord toko/keranjang dengan slash command')"><b>🛒 Bot Toko</b><span>Keranjang, checkout, payment log</span></div><div class=p-card onclick="useP('Fix error code ini: ')"><b>🔧 Fix Error</b><span>Paste error, langsung dibenerin</span></div></div></div>`;}
function useP(t){document.getElementById('msg').value=t;document.getElementById('msg').focus();autoGrow(document.getElementById('msg'))}
function addCopyButtons(){document.querySelectorAll('pre').forEach(pre=>{if(pre.querySelector('.copy-btn'))return;let b=document.createElement('button');b.className='copy-btn';b.textContent='Copy';b.onclick=()=>{navigator.clipboard.writeText(pre.querySelector('code')?.innerText||pre.innerText);b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1200)};pre.style.position='relative';pre.appendChild(b);})}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach((m,i)=>{let d=document.createElement('div');d.className='msg';let isU=m.role==='user';d.innerHTML=`<div class="avatar ${isU?'u':'y'}">${isU?'U':'Y'}</div><div class=bubble><div class=content>${isU?esc(m.content):marked.parse(m.content)}</div>${!isU?`<div class=actions><button class=act onclick="copyMsg(${i})">📋 Copy</button><button class=act onclick="regen(${i})">🔄 Regenerate</button></div>`:''}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));addCopyButtons();document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
function copyMsg(i){let ch=chats.find(c=>c.id===cur);navigator.clipboard.writeText(ch.messages[i].content);alert('Copied!')}
function regen(i){let ch=chats.find(c=>c.id===cur);if(i>0){let userMsg=ch.messages[i-1].content;ch.messages.splice(i,1);save();document.getElementById('msg').value=userMsg;sendMsg();}}
function autoGrow(el){el.style.height='24px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
async function sendMsg(){let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,40);ch.messages.push({role:'user',content:t});input.value='';autoGrow(input);renderC();save();let idx=ch.messages.length;ch.messages.push({role:'assistant',content:'⚡ Yukio Aurora mikir...'});renderC();document.getElementById('send').disabled=true;try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:ch.messages.slice(-8)})});let j=await r.json();ch.messages[idx].content=j.reply;}catch(e){ch.messages[idx].content='Error: '+e+'. Cek koneksi / API Key JUICE_KEY di Vercel.'}document.getElementById('send').disabled=false;renderC();save();}
function exportChats(){let ch=chats.find(c=>c.id===cur);if(!ch||!ch.messages.length)return alert('Chat kosong');let md='# '+ch.title+'\\n\\n'+ch.messages.map(m=>`## ${m.role}\\n${m.content}`).join('\\n\\n');let blob=new Blob([md],{type:'text/markdown'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=ch.title.replace(/\\W+/g,'_')+'.md';a.click();}
function clearAll(){if(confirm('Hapus semua chat?')){localStorage.clear();chats=[];cur=null;newChat();renderH();}}
function startVoice(){let SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return alert('Browser tidak support voice');let rec=new SR();rec.lang='id-ID';rec.start();rec.onresult=e=>{document.getElementById('msg').value=e.results[0][0].transcript;autoGrow(document.getElementById('msg'))};}
function toggleTheme(){alert('V4 Aurora saat ini dark only - light mode coming soon!')}
if(!chats.length)newChat();renderH();renderC();if(chats.find(c=>c.id===cur)?.messages?.length===0)renderW();
</script></body></html>
'''

# SATU ROUTE HANDLE SEMUA - ANTI NOT FOUND & ANTI JSON ERROR
@app.route("/", methods=["GET","POST"])
@app.route("/api/index", methods=["GET","POST"])
def main_route():
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            msg = data.get("message","").strip()
            hist = data.get("history",[])[:8]
            if not msg:
                return jsonify({"reply":"Ketik dulu bos!"})
            if not JUICE_KEY:
                return jsonify({"reply":"⚠️ JUICE_KEY belum di-set di Vercel > Settings > Environment Variables. Set JUICE_KEY = tj_xxx kamu lalu Redeploy."})
            headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type":"application/json"}
            messages = [{"role":"system","content":"Kamu Yukio AI V4 Aurora by Yukioshop. Kamu expert coding Discord bot (discord.js v14), website modern, Python, Next.js. Jawab dengan bahasa Indonesia santai tapi profesional. Selalu kasih kode lengkap dengan markdown code block, highlight, dan penjelasan step-by-step. Jika user minta bot ticket, kasih button, embed, transcript HTML."}]
            for h in hist:
                if h.get("role") in ["user","assistant"]:
                    messages.append({"role":h["role"],"content":h["content"][:2000]})
            messages.append({"role":"user","content":msg})
            payload = {"model":"deepseek-ai/DeepSeek-V4.1-Flash-1017","messages":messages,"max_tokens":4000,"temperature":0.7}
            r = requests.post(API_URL, headers=headers, json=payload, timeout=25)
            if r.status_code != 200:
                return jsonify({"reply": f"Error API {r.status_code}: {r.text[:600]}"})
            reply = r.json()["choices"][0]["message"]["content"]
            return jsonify({"reply":reply})
        except Exception as e:
            return jsonify({"reply":f"Error V4: {e}"})
    else:
        return HTML_PAGE

@app.route("/<path:path>", methods=["GET","POST"])
def catch_all(path):
    return main_route()
