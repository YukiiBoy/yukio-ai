from flask import Flask, request, jsonify
import os, requests, urllib.parse, random
app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio V7 Fixed - Free AI</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root{--bg:#06070d;--card:#151622;--border:#23243a;--primary:#8b5cf6;--primary2:#3b82f6;--text:#f8f8ff;--muted:#9a9ab8}
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(800px 400px at 20% -10%, rgba(139,92,246,.25), transparent),var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:#11111a;border-right:1px solid var(--border);display:flex;flex-direction:column;padding:14px;gap:10px}
#main{flex:1;display:flex;flex-direction:column}#topbar{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;gap:10px;align-items:center}
#chat{flex:1;overflow-y:auto;padding:20px 0}.chat-inner{max-width:800px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:24px}
.msg{display:flex;gap:12px}.avatar{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-weight:800}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.7;font-size:14px}#inputArea{padding:12px 16px 18px}.input-wrap{max-width:800px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:8px 8px 8px 16px;display:flex;gap:8px;align-items:flex-end}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;font-family:inherit}
#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer}
#previewPanel{width:0;overflow:hidden;border-left:1px solid var(--border);background:#0d0e19;display:flex;flex-direction:column;transition:.35s}#previewPanel.open{width:50%}@media(max-width:900px){#previewPanel.open{position:fixed;inset:0;width:100%;z-index:200}}
</style></head>
<body>
<div id="sidebar"><div style="padding:8px;font-weight:800">Yukio V7 FIXED<br><span style="font-size:10px;color:var(--muted)">FREE AI • Anti Char 0</span></div><button onclick="newChat()" style="width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:12px;color:#fff;font-weight:700;cursor:pointer">+ New Project</button><div id="history" style="flex:1;overflow-y:auto"></div></div>
<div id="main"><div id="topbar"><div style="flex:1;font-weight:700">✅ Yukio V7 - Fixed Free AI</div><button onclick="togglePreview()" style="padding:6px 12px;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);cursor:pointer">👁️ Preview</button></div><div id="chat"><div class="chat-inner" id="chatInner"></div></div><div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Bikinin portfolio glassmorphism dengan project showcase..." rows="1" oninput="this.style.height='24px';this.style.height=this.scrollHeight+'px'" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendMsg()}"></textarea><button id="send" onclick="sendMsg()">↑</button></div></div></div>
<div id="previewPanel"><div style="padding:12px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between"><b>Live Preview</b><button onclick="togglePreview()">✕</button></div><iframe id="previewFrame" style="flex:1;border:none;background:#fff"></iframe></div>
<script>
let chats=JSON.parse(localStorage.getItem('yukio_v7f')||'[]');let cur=localStorage.getItem('yukio_v7f_cur')||null;let lastHTML='';
function togglePreview(){document.getElementById('previewPanel').classList.toggle('open');}
function save(){localStorage.setItem('yukio_v7f',JSON.stringify(chats));localStorage.setItem('yukio_v7f_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Project',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.style.cssText='padding:10px 12px;border-radius:12px;cursor:pointer;font-size:13px;color:var(--muted)';if(c.id===cur)d.style.background='var(--card)';d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC()};h.appendChild(d);})}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML='<div style="text-align:center;padding:40px"><h1 style="font-size:28px">✅ FIXED Anti Char 0!</h1><p style="color:var(--muted);margin-top:8px">Sekarang pakai AI gratis tanpa token. Coba: Bikinin portfolio glassmorphism</p></div>';}
function extractHTML(text){let m=text.match(/```html([\\s\\S]*?)```/i);if(m)return m[1].trim();if(text.includes('<!DOCTYPE')||text.includes('<html')){let s=text.indexOf('<!DOCTYPE')!=-1?text.indexOf('<!DOCTYPE'):text.indexOf('<html');return text.slice(s);}return null;}
function updatePreview(html){lastHTML=html;document.getElementById('previewFrame').srcdoc=html;document.getElementById('previewPanel').classList.add('open');}
async function sendMsg(){let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});input.value='';renderC();save();let div=document.createElement('div');div.className='msg';div.innerHTML='<div class=\"avatar y\">Y</div><div class=bubble><div class=content>⚡ Yukio Free AI ngetik...</div></div>';document.getElementById('chatInner').appendChild(div);let contentEl=div.querySelector('.content');try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:ch.messages.slice(-6)})});let j=await r.json();contentEl.innerHTML=marked.parse(j.reply);let html=extractHTML(j.reply);if(html){lastHTML=html;contentEl.insertAdjacentHTML('beforeend','<div style=\"margin-top:10px\"><button onclick=\"updatePreview(lastHTML)\" style=\"padding:8px 16px;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;border:none;border-radius:20px;cursor:pointer;font-size:12px\">👁️ Live Preview</button></div>');}ch.messages.push({role:'assistant',content:j.reply});save();}catch(e){contentEl.textContent='Error: '+e}}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';d.innerHTML='<div class=\"avatar '+(m.role==='user'?'u\">U':'y\">Y')+'</div><div class=bubble>'+(m.role==='user'?m.content.replace(/</g,'&lt;'):marked.parse(m.content))+'</div>';inner.appendChild(d);});}
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
            
            # === FIX UTAMA: PAKAI FREE AI, GAK PAKAI r.json() YANG BIKIN CHAR 0 ===
            reply = None
            try:
                prompt = f"You are Yukio AI V7 Web Builder Expert. Build modern glassmorphism portfolio. User: {msg}. Give full single HTML file with inline CSS, dark aurora, glassmorphism."
                encoded = urllib.parse.quote(prompt)
                # Pollinations FREE - tanpa token, tanpa r.json()
                r = requests.get(f"https://text.pollinations.ai/{encoded}?model=openai&seed={random.randint(1,999999)}", timeout=40)
                if r.status_code == 200 and len(r.text.strip()) > 30:
                    reply = r.text.strip()
            except Exception as e:
                print(f"Pollinations error: {e}")

            # Fallback template kalau AI rame
            if not reply:
                reply = """Berikut portfolio glassmorphism premium - bisa langsung preview!

```html
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Portfolio Glassmorphism</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:#06070d;color:#fff;overflow-x:hidden}
.nav{padding:20px 40px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #23243a}
.hero{padding:80px 40px;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;max-width:1200px;margin:0 auto}
.hero h1{font-size:56px;font-weight:800;line-height:.9;background:linear-gradient(135deg,#fff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.glass{background:linear-gradient(135deg,rgba(255,255,255,.08),rgba(255,255,255,.02));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:24px}
.projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;max-width:1200px;margin:40px auto;padding:0 40px}
.card{background:#151622;border:1px solid #23243a;border-radius:16px;padding:20px;transition:.3s}.card:hover{transform:translateY(-4px);border-color:#8b5cf6}
</style></head><body>
<div class=nav><b>Yukio.dev</b><div>Projects • About • Contact</div></div>
<div class=hero><div><h1>Web Developer<br>Crafting Digital<br>Experiences</h1><p style="color:#9a9ab8;margin:16px 0">Specialist in glassmorphism, aurora, modern web</p><button style="padding:14px 28px;background:linear-gradient(135deg,#8b5cf6,#3b82f6);border:none;border-radius:12px;color:#fff;font-weight:700">View Projects →</button></div><div class=glass><h3>🚀 50+ Projects</h3><p style="color:#9a9ab8">SaaS, Portfolio, Dashboard</p></div></div>
<div class=projects><div class=card><h3>🚀 SaaS Landing</h3><p style="color:#9a9ab8">Dark aurora with pricing</p></div><div class=card><h3>💼 Portfolio Pro</h3><p style="color:#9a9ab8">Glassmorphism bento grid</p></div><div class=card><h3>📊 Admin Dashboard</h3><p style="color:#9a9ab8">Modern dark with chart</p></div></div>
</body></html>
