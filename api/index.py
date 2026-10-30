from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"

HTML_PAGE = '''
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI V6 • Web Builder</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#06070d;--bg2:#0d0e19;--card:#151622;--card2:#1c1d2f;--card3:#24253a;--border:#23243a;--border2:#2f304d;--primary:#8b5cf6;--primary2:#3b82f6;--accent:#06ffa5;--text:#f8f8ff;--muted:#9a9ab8;--success:#22c55e}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(1200px 600px at 10% -10%, rgba(139,92,246,.18), transparent),radial-gradient(800px 400px at 90% 0%, rgba(59,130,246,.12), transparent),radial-gradient(600px 300px at 50% 100%, rgba(6,255,165,.06), transparent),var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:300px;background:rgba(13,14,25,.85);backdrop-filter:blur(24px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:12px;gap:10px;z-index:100;transition:.3s}
.brand{display:flex;align-items:center;gap:12px;padding:10px}.logo{width:44px;height:44px;border-radius:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 8px 24px rgba(139,92,246,.35)}
.btn-new{width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px}
.btn-new:hover{transform:translateY(-1px);box-shadow:0 12px 28px rgba(139,92,246,.4)}
.tools-section{margin-top:8px}.tools-label{font-size:10px;font-weight:700;letter-spacing:.1em;color:var(--muted);padding:8px 8px 4px}
.tool-btn{width:100%;padding:10px 12px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--muted);font-size:12px;cursor:pointer;display:flex;align-items:center;gap:10px;text-align:left;margin-top:6px;transition:.2s}.tool-btn:hover{background:var(--card2);color:var(--text);border-color:var(--border2)}
#history{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:3px;margin-top:6px}
.chat-item{padding:10px 12px;border-radius:12px;cursor:pointer;font-size:12.5px;color:var(--muted);border:1px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:.2s}.chat-item:hover{background:var(--card);color:var(--text)}.chat-item.active{background:var(--card2);color:var(--text);border-color:var(--primary);box-shadow:0 0 0 1px rgba(139,92,246,.2) inset}
#main{flex:1;display:flex;flex-direction:column;min-width:0;position:relative}
#topbar{padding:10px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;background:rgba(13,14,25,.7);backdrop-filter:blur(16px)}
.hamburger{width:38px;height:38px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:flex;align-items:center;justify-content:center;cursor:pointer}
.model-select{padding:8px 12px;background:var(--card2);border:1px solid var(--border2);border-radius:12px;color:var(--text);font-size:12px;font-weight:600;outline:none;cursor:pointer;min-width:170px}
.icon-btn{width:36px;height:36px;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--muted);cursor:pointer;display:flex;align-items:center;justify-content:center}
.icon-btn:hover{color:var(--text);border-color:var(--border2)}
#workspace{display:flex;flex:1;min-height:0}
#chatArea{flex:1;display:flex;flex-direction:column;min-width:0}
#chat{flex:1;overflow-y:auto;padding:20px 0}.chat-inner{max-width:780px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:26px}
.welcome{text-align:center;padding:20px 0}.welcome h1{font-size:34px;font-weight:800;letter-spacing:-.02em;background:linear-gradient(135deg,#fff 20%,#a78bfa 80%);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.welcome p{color:var(--muted);font-size:13px;margin-top:8px}
.templates{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:20px auto 0;max-width:640px}
.t-card{padding:14px;background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--border);border-radius:16px;cursor:pointer;text-align:left;transition:.25s;position:relative;overflow:hidden}
.t-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(139,92,246,.08),transparent);opacity:0;transition:.25s}.t-card:hover{border-color:var(--primary);transform:translateY(-2px);box-shadow:0 16px 40px rgba(0,0,0,.3)}.t-card:hover::before{opacity:1}
.t-card b{font-size:12.5px;display:block;position:relative}.t-card span{font-size:11px;color:var(--muted);position:relative}
.msg{display:flex;gap:12px;animation:fade .3s ease}.avatar{width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;box-shadow:0 6px 18px rgba(139,92,246,.3)}
.bubble{flex:1;line-height:1.75;font-size:14px;min-width:0}.bubble pre{background:#0a0b14 !important;border:1px solid var(--border);border-radius:14px;padding:14px;margin:14px 0;overflow-x:auto;position:relative}
.copy-btn{position:absolute;right:8px;top:8px;padding:6px 10px;background:var(--card3);border:1px solid var(--border);border-radius:8px;font-size:11px;color:var(--muted);cursor:pointer}
.msg-actions{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}.act{padding:6px 12px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer;display:flex;align-items:center;gap:5px}.act:hover{background:var(--card2);color:var(--text);border-color:var(--border2)}
.act.primary{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;border:none}
#previewPanel{width:0;overflow:hidden;border-left:1px solid var(--border);background:var(--bg2);display:flex;flex-direction:column;transition:.35s cubic-bezier(.4,0,.2,1)}
#previewPanel.open{width:50%}
.preview-head{padding:12px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;font-size:12px;font-weight:700}
.preview-iframe{flex:1;border:none;background:#fff;width:100%}
#inputArea{padding:12px 16px 16px;background:linear-gradient(0deg,var(--bg) 40%, transparent)}
.input-wrap{max-width:780px;margin:0 auto;background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:8px 8px 8px 16px;display:flex;gap:8px;align-items:flex-end;box-shadow:0 12px 40px rgba(0,0,0,.4),0 0 0 1px rgba(255,255,255,.02) inset;transition:.2s}
.input-wrap:focus-within{border-color:var(--primary);box-shadow:0 12px 40px rgba(0,0,0,.4),0 0 0 1px rgba(139,92,246,.25) inset}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;max-height:140px;font-family:inherit;padding:8px 0;line-height:1.6}
#send{width:40px;height:40px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer;font-weight:700;box-shadow:0 6px 16px rgba(139,92,246,.4)}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}.cursor{display:inline-block;width:7px;height:13px;background:var(--primary);animation:blink 1s infinite}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:90}
@media(max-width:1100px){#previewPanel.open{position:fixed;inset:0;top:0;left:0;width:100%;z-index:200}.templates{grid-template-columns:1fr}#sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#overlay.show{display:block}}
</style></head>
<body>
<div id="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar">
<div class="brand"><div class="logo">Y</div><div><b>Yukio Builder</b><div style="font-size:10px;color:var(--muted);letter-spacing:.08em">V6 • WEB BUILDER EDITION</div></div></div>
<button class="btn-new" onclick="newChat()">✦ New Project</button>
<div class="tools-section">
<div class="tools-label">WEB TOOLS</div>
<button class="tool-btn" onclick="toolGradient()">🎨 Gradient Generator</button>
<button class="tool-btn" onclick="toolShadow()">🌑 Shadow Generator</button>
<button class="tool-btn" onclick="toolColor()">🌈 Color Palette</button>
<button class="tool-btn" onclick="toolImage()">🖼️ AI Image Gen (Free)</button>
</div>
<div style="flex:1;overflow:hidden;display:flex;flex-direction:column"><div class="tools-label">PROJECTS</div><div id="history"></div></div>
<div style="border-top:1px solid var(--border);padding-top:10px;display:flex;gap:6px">
<button onclick="exportHTML()" class="tool-btn" style="flex:1;justify-content:center">📤 Export HTML</button>
<button onclick="toggleTheme()" class="icon-btn" title="Theme">◐</button>
</div>
</div>

<div id="main">
<div id="topbar">
<button class="hamburger" onclick="toggleSidebar()">☰</button>
<select id="modelSelect" class="model-select">
<option value="DeepSeek-V3-0324">🔥 DeepSeek-V3 - Web Expert</option>
<option value="gpt-4o-mini">⚡ GPT-4o Mini - Fast</option>
<option value="gpt-4o">🚀 GPT-4o - Smart</option>
<option value="DeepSeek-R1">🧠 R1 - Reasoning</option>
</select>
<div style="flex:1"></div>
<button class="icon-btn" onclick="togglePreview()" title="Toggle Preview">👁️</button>
<button class="icon-btn" onclick="openCommand()" title="Command (Ctrl+K)">⌘K</button>
</div>

<div id="workspace">
<div id="chatArea">
<div id="chat"><div class="chat-inner" id="chatInner"></div></div>
<div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Mau bikin web apa? Contoh: bikin landing page SaaS dark aurora..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><button id="send" onclick="sendMsg()">↑</button></div></div>
</div>

<div id="previewPanel">
<div class="preview-head"><span style="flex:1">👁️ Live Preview</span><button onclick="refreshPreview()" class="icon-btn" style="width:28px;height:28px">↻</button><button onclick="togglePreview()" class="icon-btn" style="width:28px;height:28px">✕</button></div>
<iframe id="previewFrame" class="preview-iframe"></iframe>
</div>
</div>
</div>

<script>
let currentModel=localStorage.getItem('yukio_model')||'DeepSeek-V3-0324';
document.getElementById('modelSelect').value=currentModel;
let chats=JSON.parse(localStorage.getItem('yukio_v6')||'[]');let cur=localStorage.getItem('yukio_v6_cur')||null;
let lastHTML='';
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function togglePreview(){document.getElementById('previewPanel').classList.toggle('open');}
function save(){localStorage.setItem('yukio_v6',JSON.stringify(chats));localStorage.setItem('yukio_v6_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Project',model:currentModel,messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC();if(innerWidth<=1100)toggleSidebar()};h.appendChild(d);})}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML=`<div class=welcome><h1>Mau bikin web apa hari ini?</h1><p>Yukio V6 bisa bikin & preview langsung!</p><div class=templates>
<div class=t-card onclick="useT('Bikinin landing page SaaS modern dark aurora dengan pricing, testimoni, CTA')"><b>🚀 SaaS Landing Page</b><span>Hero, pricing, testimonial, dark aurora</span></div>
<div class=t-card onclick="useT('Bikinin portfolio web developer keren glassmorphism dengan project showcase')"><b>💼 Portfolio Pro</b><span>Glassmorphism, animasi, project grid</span></div>
<div class=t-card onclick="useT('Bikinin dashboard admin modern dengan chart, sidebar, dark mode')"><b>📊 Admin Dashboard</b><span>Sidebar, chart, table, responsive</span></div>
<div class=t-card onclick="useT('Bikinin toko online / e-commerce product page modern')"><b>🛒 E-Commerce Page</b><span>Product, cart, checkout UI</span></div>
</div></div>`;}
function useT(t){document.getElementById('msg').value=t;autoGrow(document.getElementById('msg'));document.getElementById('msg').focus();}
function autoGrow(el){el.style.height='24px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
function addCopy(){document.querySelectorAll('pre').forEach(pre=>{if(pre.querySelector('.copy-btn'))return;let b=document.createElement('button');b.className='copy-btn';b.textContent='Copy';b.onclick=()=>{navigator.clipboard.writeText(pre.querySelector('code')?.innerText||pre.innerText);b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1000)};pre.appendChild(b);})}
function extractHTML(text){let m=text.match(/```html([\\s\\S]*?)```/i)||text.match(/```([\\s\\S]*?<html[\\s\\S]*?)```/i);if(m)return m[1].trim();if(text.includes('<!DOCTYPE')||text.includes('<html')){let start=text.indexOf('<!DOCTYPE')!=-1?text.indexOf('<!DOCTYPE'):text.indexOf('<html');return text.slice(start);}return null;}
function updatePreview(html){lastHTML=html;let frame=document.getElementById('previewFrame');frame.srcdoc=html;document.getElementById('previewPanel').classList.add('open');}
function refreshPreview(){if(lastHTML)document.getElementById('previewFrame').srcdoc=lastHTML;}
function openCommand(){let cmd=prompt('⌘ Command Palette:\\n- gradient\\n- shadow\\n- color\\n- image [prompt]\\n- export');if(!cmd)return;if(cmd.includes('gradient'))toolGradient();else if(cmd.includes('shadow'))toolShadow();else if(cmd.includes('color'))toolColor();else if(cmd.startsWith('image'))toolImage(cmd.replace('image','').trim());else if(cmd.includes('export'))exportHTML();}
function toolGradient(){let g=prompt('Gradient (contoh: 135deg, #8b5cf6, #3b82f6)','135deg, #8b5cf6, #3b82f6');if(g)sendMsgDirect(`Bikinin CSS gradient keren: linear-gradient(${g}) + contoh penggunaannya di button & card`);}
function toolShadow(){sendMsgDirect('Bikinin koleksi box-shadow modern untuk card, button, modal - dari soft sampai dramatic - kasih contoh CSS nya');}
function toolColor(){sendMsgDirect('Bikinin color palette modern untuk web SaaS dark mode: primary, secondary, accent, background, text - kasih hex code + contoh pakai di Tailwind');}
function toolImage(prompt=''){let p=prompt||prompt('Mau gambar apa? (AI free Pollinations)','modern saas dashboard dark aurora');if(!p)return;let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(p)}?width=1024&height=768&nologo=true`;let ch=chats.find(c=>c.id===cur);ch.messages.push({role:'assistant',content:`![Generated](${url})\\n\\n**Image URL:** \`${url}\`\\n\\nBisa langsung pakai di <img> tag!`});renderC();save();}
function exportHTML(){if(!lastHTML)return alert('Belum ada HTML untuk di-export! Minta AI bikin web dulu.');let blob=new Blob([lastHTML],{type:'text/html'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=(chats.find(c=>c.id===cur)?.title||'yukio-web')+'.html';a.click();}
function sendMsgDirect(t){document.getElementById('msg').value=t;sendMsg();}
async function typeWriter(el, text, onChunk){
  return new Promise(res=>{
    let i=0;function step(){
      if(i<text.length){
        let chunk=text.slice(0,i+30);
        try{el.innerHTML=marked.parse(chunk)+'<span class=cursor></span>'}catch{el.textContent=chunk}
        if(onChunk)onChunk(chunk);
        i+=30;document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;setTimeout(step,8);
      }else{el.innerHTML=marked.parse(text);el.querySelectorAll&&el.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));addCopy();let html=extractHTML(text);if(html){el.insertAdjacentHTML('beforeend',`<div class=msg-actions><button class="act primary" onclick="updatePreview(lastHTML)">👁️ Preview</button><button class=act onclick="navigator.clipboard.writeText(lastHTML);this.textContent='Copied!'">📋 Copy HTML</button><button class=act onclick="exportHTML()">📤 Export</button></div>`);lastHTML=html;}res();}
    }step();
  });
}
async function sendMsg(){
  let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;currentModel=document.getElementById('modelSelect').value;localStorage.setItem('yukio_model',currentModel);
  let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,35);
  ch.messages.push({role:'user',content:t});input.value='';autoGrow(input);renderC();save();
  let div=document.createElement('div');div.className='msg';div.innerHTML=`<div class="avatar y">Y</div><div class=bubble><div class=content>⚡ ${currentModel.split('-')[0]} ngetik<span class=cursor></span></div></div>`;
  document.getElementById('chatInner').appendChild(div);let contentEl=div.querySelector('.content');
  document.getElementById('send').disabled=true;
  try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:ch.messages.slice(-8),model:currentModel})});let j=await r.json();await typeWriter(contentEl,j.reply);ch.messages.push({role:'assistant',content:j.reply});save();}catch(e){contentEl.textContent='Error: '+e}
  document.getElementById('send').disabled=false;
}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';let html=m.role==='assistant'?extractHTML(m.content):null;let extra=html?`<div class=msg-actions><button class="act primary" onclick="updatePreview(\`${html.replace(/`/g,'\\\\`').replace(/\\$/g,'\\\\$')}\`)">👁️ Preview</button><button class=act onclick="exportHTML()">📤 Export</button></div>`:'';d.innerHTML=`<div class="avatar ${m.role==='user'?'u':'y'}">${m.role==='user'?'U':'Y'}</div><div class=bubble><div class=content>${m.role==='user'?esc(m.content):marked.parse(m.content)}</div>${m.role==='assistant'?extra:''}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));addCopy();document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
function toggleTheme(){document.body.style.filter=document.body.style.filter?'':'invert(1) hue-rotate(180deg)';}
if(!chats.length)newChat();renderH();renderC();
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();openCommand();}});
</script></body></html>
'''

@app.route("/", methods=["GET","POST"])
@app.route("/api/index", methods=["GET","POST"])
def main_route():
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            msg = data.get("message","").strip()
            model = data.get("model","DeepSeek-V3-0324")
            hist = data.get("history",[])[:8]
            if not msg:
                return jsonify({"reply":"Ketik dulu bos!"})
            if not GITHUB_TOKEN:
                return jsonify({"reply":"⚠️ GITHUB_TOKEN belum di-set di Vercel! Buat di github.com/settings/tokens"})
            headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type":"application/json"}
            messages = [{"role":"system","content":"Kamu Yukio AI V6 Web Builder Expert by Yukioshop. Kamu jago bikin website modern: landing page SaaS, portfolio glassmorphism, dashboard, e-commerce. Selalu kasih HTML lengkap single file dengan CSS inline modern (aurora, glassmorphism, gradient, shadow). Pakai font Plus Jakarta Sans. Buat responsive, dark mode, animasi halus. Jangan pakai external CSS kecuali Google Fonts. Output HTML harus bisa langsung preview."}]
            for h in hist:
                if h.get("role") in ["user","assistant"]:
                    messages.append({"role":h["role"],"content":h["content"][:2500]})
            messages.append({"role":"user","content":msg})
            payload = {"model": model, "messages": messages, "max_tokens": 6000, "temperature": 0.7}
            r = requests.post(API_URL, headers=headers, json=payload, timeout=35)
            if r.status_code != 200:
                return jsonify({"reply": f"Error {r.status_code}: {r.text[:600]} Coba ganti model!"})
            # GANTI BAGIAN INI DI CODE LAMA LU:
# r = requests.post(...)
# reply = r.json()["choices"][0]["message"]["content"]  <-- INI YANG BIKIN ERROR CHAR 0

# JADI INI:
if not r.text or r.status_code != 200:
    return jsonify({"reply": f"Error GitHub {r.status_code}: {r.text[:500]} - Coba ganti model ke gpt-4o-mini"})
try:
    j = r.json()
    reply = j["choices"][0]["message"]["content"]
except:
    # Fallback ke Pollinations kalau GitHub ngasih kosong
    pr = requests.get(f"https://text.pollinations.ai/{requests.utils.quote(msg)}", timeout=15)
    reply = pr.text if pr.status_code==200 else f"Error parse: {r.text[:500]}"
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"reply": f"Error: {e}"})
    else:
        return HTML_PAGE

@app.route("/<path:path>", methods=["GET","POST"])
def catch_all(path):
    return main_route()
