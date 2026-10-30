from flask import Flask, request, jsonify
import requests
import urllib.parse
import random

# ==============================
# INI WAJIB ADA DI TOP LEVEL UNTUK VERCEL!
# JANGAN DIHAPUS ATAU DIPINDAH!
# ==============================
app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI V8 - Free Web Builder</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
:root{--bg:#06070d;--card:#151622;--card2:#1c1d2f;--border:#23243a;--primary:#8b5cf6;--primary2:#3b82f6;--text:#f8f8ff;--muted:#9a9ab8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(900px 500px at 20% -10%, rgba(139,92,246,.25), transparent),radial-gradient(600px 400px at 90% 0%, rgba(59,130,246,.15), transparent),var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:rgba(17,17,26,.95);backdrop-filter:blur(20px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:14px;gap:10px}
.brand{display:flex;gap:12px;align-items:center;padding:6px}.logo{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 8px 20px rgba(139,92,246,.4)}
.btn-new{width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:12px;color:#fff;font-weight:700;cursor:pointer;box-shadow:0 6px 16px rgba(139,92,246,.35)}
.tool{width:100%;padding:10px 12px;background:var(--card);border:1px solid var(--border);border-radius:10px;color:var(--muted);font-size:12px;text-align:left;cursor:pointer;margin-top:6px}.tool:hover{background:var(--card2);color:var(--text)}
#history{flex:1;overflow-y:auto;margin-top:8px;display:flex;flex-direction:column;gap:4px}
.chat-item{padding:9px 12px;border-radius:10px;cursor:pointer;font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chat-item:hover,.chat-item.active{background:var(--card);color:var(--text)}
#main{flex:1;display:flex;flex-direction:column;min-width:0}
#topbar{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;background:rgba(13,14,25,.7)}
#chat{flex:1;overflow-y:auto;padding:20px 0}.chat-inner{max-width:800px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:24px}
.welcome{text-align:center;padding:30px 0}.welcome h1{font-size:32px;font-weight:800;background:linear-gradient(135deg,#fff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.msg{display:flex;gap:12px}.avatar{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff}
.bubble{flex:1;line-height:1.7;font-size:14px;min-width:0}.bubble pre{background:#0e0e17;border:1px solid var(--border);border-radius:12px;padding:12px;margin:12px 0;overflow:auto}
#inputArea{padding:12px 16px 18px}.input-wrap{max-width:800px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:24px;padding:8px 8px 8px 16px;display:flex;gap:8px;align-items:flex-end;box-shadow:0 12px 30px rgba(0,0,0,.4)}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;max-height:120px;font-family:inherit}
#send{width:38px;height:38px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer;font-weight:700}
#previewPanel{width:0;overflow:hidden;border-left:1px solid var(--border);background:#0d0e19;display:flex;flex-direction:column;transition:.35s}#previewPanel.open{width:50%}
.preview-iframe{flex:1;border:none;background:#fff;width:100%}
@media(max-width:1000px){#previewPanel.open{position:fixed;inset:0;width:100%;z-index:200}}
</style>
</head>
<body>
<div id="sidebar">
<div class="brand"><div class="logo">Y</div><div><b>Yukio AI V8</b><div style="font-size:10px;color:var(--muted)">FREE AI • NO TOKEN • 0 ERROR</div></div></div>
<button class="btn-new" onclick="newChat()">+ New Project</button>
<div style="font-size:10px;color:var(--muted);letter-spacing:.1em;margin-top:4px">WEB TOOLS FREE</div>
<button class="tool" onclick="quick('Bikinin 5 gradient modern dark aurora untuk button dan card')">🎨 Gradient Generator</button>
<button class="tool" onclick="quick('Bikinin koleksi box-shadow dan glow modern untuk card')">🌑 Shadow & Glow</button>
<button class="tool" onclick="genImage()">🖼️ AI Image Gen Free</button>
<button class="tool" onclick="quick('Bikinin color palette SaaS dark mode lengkap')">🌈 Color Palette</button>
<div style="flex:1;display:flex;flex-direction:column;overflow:hidden;margin-top:8px"><div style="font-size:10px;color:var(--muted);letter-spacing:.1em">PROJECTS</div><div id="history"></div></div>
<div style="display:flex;gap:6px;border-top:1px solid var(--border);padding-top:10px">
<button onclick="exportHTML()" style="flex:1;padding:10px;background:var(--card);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:12px;cursor:pointer">📤 Export HTML</button>
</div>
</div>

<div id="main">
<div id="topbar"><div style="flex:1;font-weight:700">Yukio V8 - 0 Error • Free AI</div><div style="padding:4px 10px;background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.3);border-radius:20px;font-size:10px;color:#22c55e;font-weight:700">● FREE FOREVER</div><button onclick="togglePreview()" style="padding:6px 12px;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--text);cursor:pointer">👁️ Preview</button></div>
<div id="chat"><div class="chat-inner" id="chatInner"></div></div>
<div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Bikinin web apa hari ini? Contoh: portfolio glassmorphism, landing page SaaS..." rows="1" oninput="this.style.height='24px';this.style.height=this.scrollHeight+'px'" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendMsg()}"></textarea><button id="send" onclick="sendMsg()">↑</button></div>
<div style="max-width:800px;margin:8px auto 0;display:flex;gap:6px;flex-wrap:wrap">
<button onclick="quick('Bikinin landing page SaaS dark aurora dengan hero, pricing 3 tier, testimoni, FAQ')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">🚀 SaaS</button>
<button onclick="quick('Bikinin portfolio web developer glassmorphism dengan project showcase bento grid')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">💼 Portfolio</button>
<button onclick="quick('Bikinin dashboard admin modern dark dengan sidebar dan chart')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">📊 Dashboard</button>
</div></div>
</div>

<div id="previewPanel"><div style="padding:12px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;background:var(--card)"><b>👁️ Live Preview</b><div style="display:flex;gap:6px"><button onclick="refreshPreview()" style="padding:4px 8px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);cursor:pointer">↻</button><button onclick="togglePreview()" style="padding:4px 8px;border-radius:8px;border:1px solid var(--border);background:var(--card);color:var(--text);cursor:pointer">✕</button></div></div><iframe id="previewFrame" class="preview-iframe"></iframe></div>

<script>
let chats=JSON.parse(localStorage.getItem('yukio_v8')||'[]');let cur=localStorage.getItem('yukio_v8_cur')||null;let lastHTML='';
function togglePreview(){document.getElementById('previewPanel').classList.toggle('open');}
function refreshPreview(){if(lastHTML)document.getElementById('previewFrame').srcdoc=lastHTML;}
function save(){localStorage.setItem('yukio_v8',JSON.stringify(chats));localStorage.setItem('yukio_v8_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Project',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC()};h.appendChild(d);})}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML='<div class="welcome"><h1>Yukio AI V8<br>0 Error - Free AI</h1><p style="color:var(--muted);font-size:13px;margin-top:10px">✅ Build Fixed • ✅ Free AI • ✅ Live Preview • ✅ Export<br>Coba klik template di bawah:</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px;max-width:600px;margin-left:auto;margin-right:auto"><div onclick="quick(\'Bikinin landing page SaaS dark aurora dengan hero, pricing 3 tier, testimoni, FAQ, CTA\')" style="padding:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;cursor:pointer;text-align:left"><b style="font-size:13px">🚀 SaaS Landing</b><br><span style="font-size:11px;color:var(--muted)">Hero aurora, pricing, FAQ</span></div><div onclick="quick(\'Bikinin portfolio web developer keren glassmorphism dengan bento grid project showcase\')" style="padding:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;cursor:pointer;text-align:left"><b style="font-size:13px">💼 Portfolio Pro</b><br><span style="font-size:11px;color:var(--muted)">Glassmorphism, animasi</span></div></div></div>';}
function extractHTML(t){let m=t.match(/```html([\\s\\S]*?)```/i);if(m)return m[1].trim();if(t.toLowerCase().includes('<!doctype')||t.toLowerCase().includes('<html')){let s=t.toLowerCase().indexOf('<!doctype');if(s==-1)s=t.toLowerCase().indexOf('<html');return t.slice(s, s+25000);}return null;}
function updatePreview(h){lastHTML=h;document.getElementById('previewFrame').srcdoc=h;document.getElementById('previewPanel').classList.add('open');}
function exportHTML(){if(!lastHTML)return alert('Belum ada HTML! Bikin web dulu bos.');let blob=new Blob([lastHTML],{type:'text/html'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='yukio-web-'+Date.now()+'.html';a.click();}
function quick(t){document.getElementById('msg').value=t;sendMsg();}
function genImage(){let p=prompt('Mau gambar apa? (AI Free Pollinations)','modern saas dashboard dark aurora minimal');if(!p)return;let url='https://image.pollinations.ai/prompt/'+encodeURIComponent(p)+'?width=1280&height=720&nologo=true&seed='+Math.floor(Math.random()*10000);let ch=chats.find(c=>c.id===cur);ch.messages.push({role:'assistant',content:'![Generated]('+url+')\\n\\n**Prompt:** '+p+'\\n\\n**HTML:**\\n```html\\n<img src=\\"'+url+'\\" alt=\\"'+p+'\\" style=\\"width:100%;border-radius:16px\\" />\\n```'});renderC();save();}
async function sendMsg(){let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);ch.messages.push({role:'user',content:t});input.value='';renderC();save();let div=document.createElement('div');div.className='msg';div.innerHTML='<div class="avatar y">Y</div><div class=bubble><div class=content>⚡ Yukio Free AI ngetik...</div></div>';document.getElementById('chatInner').appendChild(div);let contentEl=div.querySelector('.content');let chatDiv=document.getElementById('chat');chatDiv.scrollTop=chatDiv.scrollHeight;try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:ch.messages.slice(-6)})});let j=await r.json();contentEl.innerHTML=marked.parse(j.reply);let html=extractHTML(j.reply);if(html){lastHTML=html;contentEl.insertAdjacentHTML('beforeend','<div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap"><button onclick="updatePreview(lastHTML)" style="padding:8px 16px;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;border:none;border-radius:20px;cursor:pointer;font-size:12px">👁️ Live Preview</button><button onclick="exportHTML()" style="padding:8px 16px;background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:20px;cursor:pointer;font-size:12px">📤 Export HTML</button></div>');}ch.messages.push({role:'assistant',content:j.reply});save();}catch(e){contentEl.textContent='Error: '+e}chatDiv.scrollTop=chatDiv.scrollHeight;}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';d.innerHTML='<div class="avatar '+(m.role==='user'?'u">U':'y">Y')+'</div><div class=bubble>'+(m.role==='user'?m.content.replace(/</g,'&lt;'):marked.parse(m.content))+'</div>';inner.appendChild(d);});document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
if(!chats.length)newChat();renderH();renderC();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return HTML_PAGE
    
    # POST - Chat dengan Free AI
    try:
        data = request.get_json(silent=True) or {}
        msg = data.get("message", "").strip()
        
        if not msg:
            return jsonify({"reply": "Ketik dulu bos! Mau bikin web apa?"})

        # FREE AI - POLLINATIONS (TANPA TOKEN!)
        # Ini tidak pakai r.json() jadi tidak akan error char 0
        reply = None
        try:
            # Prompt untuk web builder
            system = "You are Yukio AI V8 - Expert Web Builder. Create modern website. Always output full HTML single file with inline CSS. Style: dark aurora, glassmorphism, modern, Plus Jakarta Sans font. "
            full_prompt = system + "User request: " + msg + ". Create website, output HTML in ```html code block."
            
            # Encode untuk URL
            encoded = urllib.parse.quote(full_prompt[:2500])
            seed = random.randint(1, 999999)
            
            # Pollinations FREE - model openai (gratis & stabil)
            url = f"https://text.pollinations.ai/{encoded}?model=openai&seed={seed}"
            
            r = requests.get(url, timeout=45, headers={"User-Agent": "YukioAI/8.0"})
            
            if r.status_code == 200 and r.text and len(r.text.strip()) > 30:
                reply = r.text.strip()
        except Exception as e:
            print(f"Free AI error: {e}")
            reply = None

        # FALLBACK TEMPLATE - BIAR TIDAK PERNAH ERROR KOSONG
        if not reply or len(reply.strip()) < 40:
            reply = """AI gratis lagi rame bos, tapi ini template portfolio glassmorphism premium - bisa langsung preview & export:

```html
<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Portfolio Glassmorphism</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Plus Jakarta Sans',sans-serif;background:#06070d;color:#fff;overflow-x:hidden}
.nav{padding:20px 40px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #23243a}
.hero{padding:80px 40px;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;max-width:1200px;margin:0 auto}
.hero h1{font-size:clamp(32px,5vw,56px);font-weight:800;line-height:.9;background:linear-gradient(135deg,#fff 30%,#a78bfa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.glass{background:linear-gradient(135deg,rgba(255,255,255,.08),rgba(255,255,255,.02));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:24px}
.projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;max-width:1200px;margin:40px auto;padding:0 40px}
.card{background:#151622;border:1px solid #23243a;border-radius:16px;padding:22px;transition:.3s}.card:hover{transform:translateY(-4px);border-color:#8b5cf6;box-shadow:0 20px 40px rgba(139,92,246,.15)}
.badge{padding:5px 10px;background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.3);border-radius:20px;font-size:11px;color:#a78bfa}
.btn{padding:14px 28px;background:linear-gradient(135deg,#8b5cf6,#3b82f6);border:none;border-radius:12px;color:#fff;font-weight:700;cursor:pointer;box-shadow:0 8px 20px rgba(139,92,246,.35)}
</style></head><body>
<div class=nav><b>YUKIO.DEV</b><div style="color:#9a9ab8;font-size:13px">Projects • About • Contact</div></div>
<div class=hero><div><div class=badge>✨ Available for work</div><h1 style="margin-top:12px">Web Developer<br>Crafting<br>Digital Magic</h1><p style="color:#9a9ab8;margin:16px 0;line-height:1.6">Specialist in glassmorphism, aurora, modern web. Building fast, beautiful, functional websites.</p><button class=btn>View Projects →</button></div><div class=glass><h3>🚀 Stats</h3><div style="margin-top:12px;color:#9a9ab8;line-height:2;font-size:14px">50+ Projects Delivered<br>10+ Happy Clients<br>2 Years Experience<br>100% Free AI Powered</div></div></div>
<div class=projects>
<div class=card><h3>🚀 SaaS Dashboard</h3><p style="color:#9a9ab8;margin:8px 0;font-size:13px">Dark aurora with pricing 3 tier & analytics</p><div style="margin-top:10px"><span class=badge>React</span> <span class=badge>Tailwind</span></div></div>
<div class=card><h3>💼 Portfolio Pro</h3><p style="color:#9a9ab8;margin:8px 0;font-size:13px">Glassmorphism bento grid with modal & filter</p><div style="margin-top:10px"><span class=badge>Next.js</span> <span class=badge>Framer</span></div></div>
<div class=card><h3>🛒 E-Commerce Modern</h3><p style="color:#9a9ab8;margin:8px 0;font-size:13px">Product page with variant, cart, review</p><div style="margin-top:10px"><span class=badge>Shopify</span> <span class=badge>GSAP</span></div></div>
</div>
<div style="text-align:center;padding:50px 20px;color:#9a9ab8;font-size:12px;border-top:1px solid #23243a;margin-top:50px">© 2026 Yukio Portfolio V8 • Built with Free AI • 0 Error • Free Forever</div>
</body></html>
