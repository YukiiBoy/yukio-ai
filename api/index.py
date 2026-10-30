from flask import Flask, request, jsonify
import os, requests, urllib.parse, random
app = Flask(__name__)

# FREE AI ENDPOINTS - GAK BUTUH TOKEN!
FREE_AI_URL = "https://text.pollinations.ai/"

HTML_PAGE = '''
<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI V7 • Web Builder Free</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/tokyo-night-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{--bg:#06070d;--bg2:#0d0e19;--card:#151622;--card2:#1c1d2f;--card3:#24253a;--border:#23243a;--border2:#2f304d;--primary:#8b5cf6;--primary2:#3b82f6;--accent:#06ffa5;--text:#f8f8ff;--muted:#9a9ab8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;background:radial-gradient(1200px 600px at 10% -10%, rgba(139,92,246,.22), transparent),radial-gradient(900px 500px at 90% 0%, rgba(59,130,246,.14), transparent),radial-gradient(600px 300px at 50% 100%, rgba(6,255,165,.07), transparent),var(--bg);color:var(--text);height:100vh;display:flex;overflow:hidden}
#sidebar{width:320px;background:rgba(13,14,25,.88);backdrop-filter:blur(24px);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:12px;gap:10px;z-index:100;transition:.3s}
.brand{display:flex;align-items:center;gap:12px;padding:10px}.logo{width:44px;height:44px;border-radius:14px;background:linear-gradient(135deg,var(--primary),var(--primary2));display:flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 8px 24px rgba(139,92,246,.4)}
.btn-new{width:100%;padding:12px;background:linear-gradient(135deg,var(--primary),var(--primary2));border:none;border-radius:14px;color:#fff;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 8px 20px rgba(139,92,246,.35);transition:.2s}.btn-new:hover{transform:translateY(-1px);box-shadow:0 12px 28px rgba(139,92,246,.45)}
.tools-label{font-size:10px;font-weight:700;letter-spacing:.12em;color:var(--muted);padding:8px 8px 4px}
.tool-btn{width:100%;padding:10px 12px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--muted);font-size:12.5px;cursor:pointer;display:flex;align-items:center;gap:10px;text-align:left;margin-top:6px;transition:.2s}.tool-btn:hover{background:var(--card2);color:var(--text);border-color:var(--border2);transform:translateY(-1px)}
#history{flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:3px;margin-top:6px}
.chat-item{padding:10px 12px;border-radius:12px;cursor:pointer;font-size:12.5px;color:var(--muted);border:1px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:.2s}.chat-item:hover{background:var(--card);color:var(--text)}.chat-item.active{background:var(--card2);color:var(--text);border-color:rgba(139,92,246,.4);box-shadow:0 0 0 1px rgba(139,92,246,.15) inset}
#main{flex:1;display:flex;flex-direction:column;min-width:0}
#topbar{padding:10px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;background:rgba(13,14,25,.7);backdrop-filter:blur(16px)}
.icon-btn{width:36px;height:36px;border-radius:10px;border:1px solid var(--border);background:var(--card);color:var(--muted);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s}.icon-btn:hover{color:var(--text);border-color:var(--border2);background:var(--card2)}
.hamburger{width:38px;height:38px;border-radius:12px;border:1px solid var(--border);background:var(--card);color:var(--text);display:flex;align-items:center;justify-content:center;cursor:pointer}
#workspace{display:flex;flex:1;min-height:0}
#chatArea{flex:1;display:flex;flex-direction:column;min-width:0}
#chat{flex:1;overflow-y:auto;padding:20px 0}.chat-inner{max-width:800px;margin:0 auto;padding:0 20px;display:flex;flex-direction:column;gap:28px}
.welcome{text-align:center;padding:24px 0}.welcome h1{font-size:36px;font-weight:800;letter-spacing:-.03em;background:linear-gradient(135deg,#fff 20%,#a78bfa 70%,#60a5fa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1}
.welcome p{color:var(--muted);font-size:13px;margin-top:10px}
.templates{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:24px auto 0;max-width:660px}
.t-card{padding:16px;background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--border);border-radius:16px;cursor:pointer;text-align:left;transition:.3s;position:relative;overflow:hidden}
.t-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(139,92,246,.1),transparent);opacity:0;transition:.3s}.t-card:hover{border-color:rgba(139,92,246,.5);transform:translateY(-3px);box-shadow:0 20px 40px rgba(0,0,0,.35)}.t-card:hover::before{opacity:1}
.t-card b{font-size:13px;display:block;position:relative}.t-card span{font-size:11px;color:var(--muted);position:relative;margin-top:4px;display:block}
.msg{display:flex;gap:12px;animation:fade .35s ease}.avatar{width:36px;height:36px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0}.u{background:#fff;color:#000}.y{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;box-shadow:0 6px 18px rgba(139,92,246,.35)}
.bubble{flex:1;line-height:1.75;font-size:14.2px;min-width:0}.bubble pre{background:#0a0b14 !important;border:1px solid var(--border);border-radius:14px;padding:14px;margin:14px 0;overflow-x:auto;position:relative}
.copy-btn{position:absolute;right:8px;top:8px;padding:6px 10px;background:var(--card3);border:1px solid var(--border);border-radius:8px;font-size:11px;color:var(--muted);cursor:pointer}
.msg-actions{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}.act{padding:7px 14px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11.5px;color:var(--muted);cursor:pointer;display:flex;align-items:center;gap:6px;transition:.2s}.act:hover{background:var(--card2);color:var(--text)}.act.primary{background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;border:none;box-shadow:0 6px 16px rgba(139,92,246,.35)}
#previewPanel{width:0;overflow:hidden;border-left:1px solid var(--border);background:var(--bg2);display:flex;flex-direction:column;transition:.4s cubic-bezier(.4,0,.2,1)}
#previewPanel.open{width:50%}
.preview-head{padding:12px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;font-size:12px;font-weight:700;background:var(--card)}
.preview-iframe{flex:1;border:none;background:#fff;width:100%}
#inputArea{padding:12px 16px 18px;background:linear-gradient(0deg,var(--bg) 50%, transparent)}
.input-wrap{max-width:800px;margin:0 auto;background:var(--card);border:1px solid var(--border2);border-radius:24px;padding:8px 8px 8px 18px;display:flex;gap:10px;align-items:flex-end;box-shadow:0 16px 50px rgba(0,0,0,.45),0 0 0 1px rgba(255,255,255,.02) inset;transition:.2s}
.input-wrap:focus-within{border-color:rgba(139,92,246,.6);box-shadow:0 16px 50px rgba(0,0,0,.45),0 0 0 1px rgba(139,92,246,.3) inset}
#msg{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:14px;resize:none;min-height:24px;max-height:140px;font-family:inherit;padding:8px 0;line-height:1.6}
#send{width:42px;height:42px;border-radius:12px;border:none;background:linear-gradient(135deg,var(--primary),var(--primary2));color:#fff;cursor:pointer;font-weight:700;box-shadow:0 6px 18px rgba(139,92,246,.45);transition:.2s}#send:hover{transform:translateY(-1px)}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}.cursor{display:inline-block;width:7px;height:13px;background:var(--primary);animation:blink 1s infinite}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:90}
@media(max-width:1100px){#previewPanel.open{position:fixed;inset:0;width:100%;z-index:200}.templates{grid-template-columns:1fr}#sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}#sidebar.open{transform:translateX(0)}#overlay.show{display:block}}
</style></head>
<body>
<div id="overlay" onclick="toggleSidebar()"></div>
<div id="sidebar">
<div class="brand"><div class="logo">Y</div><div><b>Yukio AI</b><div style="font-size:10px;color:var(--muted);letter-spacing:.1em">V7 • FREE AI • BUILDER</div></div></div>
<button class="btn-new" onclick="newChat()">✦ New Project</button>
<div class="tools-label">WEB TOOLS (FREE)</div>
<button class="tool-btn" onclick="toolAction('gradient')">🎨 Gradient Generator</button>
<button class="tool-btn" onclick="toolAction('shadow')">🌑 Shadow & Glow</button>
<button class="tool-btn" onclick="toolAction('palette')">🌈 Color Palette Pro</button>
<button class="tool-btn" onclick="toolAction('image')">🖼️ AI Image Gen (Free)</button>
<button class="tool-btn" onclick="toolAction('seo')">🔍 SEO Optimizer</button>
<div style="flex:1;overflow:hidden;display:flex;flex-direction:column;margin-top:8px"><div class="tools-label">PROJECTS</div><div id="history"></div></div>
<div style="border-top:1px solid var(--border);padding-top:10px;display:flex;gap:8px">
<button onclick="exportHTML()" style="flex:1;padding:10px;background:var(--card);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:12px;cursor:pointer">📤 Export HTML</button>
<button onclick="exportZip()" class="icon-btn" title="Export ZIP">📦</button>
</div>
</div>

<div id="main">
<div id="topbar">
<button class="hamburger" onclick="toggleSidebar()">☰</button>
<div style="font-weight:700;font-size:13px;flex:1">Yukio V7 • Free AI • Anti Error</div>
<div style="padding:6px 12px;background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.25);border-radius:20px;font-size:10px;font-weight:700;color:#22c55e">● FREE FOREVER</div>
<button class="icon-btn" onclick="togglePreview()" title="Live Preview">👁️</button>
<button class="icon-btn" onclick="openCommand()" title="⌘K">⌘K</button>
</div>

<div id="workspace">
<div id="chatArea">
<div id="chat"><div class="chat-inner" id="chatInner"></div></div>
<div id="inputArea"><div class="input-wrap"><textarea id="msg" placeholder="Mau bikin web apa? Contoh: landing page SaaS dark aurora dengan pricing..." rows="1" oninput="autoGrow(this)" onkeydown="handleKey(event)"></textarea><button id="send" onclick="sendMsg()">↑</button></div><div style="max-width:800px;margin:8px auto 0;display:flex;gap:6px;flex-wrap:wrap"><button onclick="useT('Bikinin landing page SaaS dark aurora dengan pricing & testimoni')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">🚀 SaaS</button><button onclick="useT('Bikinin portfolio developer glassmorphism')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">💼 Portfolio</button><button onclick="useT('Bikinin dashboard admin modern')" style="padding:5px 10px;background:var(--card);border:1px solid var(--border);border-radius:20px;font-size:11px;color:var(--muted);cursor:pointer">📊 Dashboard</button></div></div>
</div>

<div id="previewPanel">
<div class="preview-head"><span style="flex:1">👁️ Live Preview - Web Builder</span><button onclick="refreshPreview()" class="icon-btn" style="width:28px;height:28px">↻</button><button onclick="togglePreview()" class="icon-btn" style="width:28px;height:28px">✕</button></div>
<iframe id="previewFrame" class="preview-iframe"></iframe>
</div>
</div>
</div>

<script>
let chats=JSON.parse(localStorage.getItem('yukio_v7')||'[]');let cur=localStorage.getItem('yukio_v7_cur')||null;let lastHTML='';
function toggleSidebar(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function togglePreview(){document.getElementById('previewPanel').classList.toggle('open');}
function save(){localStorage.setItem('yukio_v7',JSON.stringify(chats));localStorage.setItem('yukio_v7_cur',cur);renderH()}
function newChat(){cur=Date.now().toString();chats.unshift({id:cur,title:'New Project',messages:[]});save();renderC();}
function renderH(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===cur?' active':'');d.textContent=c.title;d.onclick=()=>{cur=c.id;save();renderC();if(innerWidth<=1100)toggleSidebar()};h.appendChild(d);})}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function renderW(){let inner=document.getElementById('chatInner');if(chats.find(c=>c.id===cur)?.messages?.length>0)return;inner.innerHTML=`<div class=welcome><h1>Bikin Web Apa<br>Hari Ini?</h1><p>Yukio V7 pakai AI gratis 100% • Live preview • Export langsung jadi</p><div class=templates>
<div class=t-card onclick="useT('Bikinin landing page SaaS modern dark aurora dengan hero, pricing 3 tier, testimoni, FAQ, CTA, footer')"><b>🚀 SaaS Landing Page</b><span>Hero aurora, pricing, testimonial, FAQ, CTA - paling laris!</span></div>
<div class=t-card onclick="useT('Bikinin portfolio web developer keren glassmorphism dengan animasi, project showcase, skills')"><b>💼 Portfolio Pro</b><span>Glassmorphism, bento grid, project modal, contact</span></div>
<div class=t-card onclick="useT('Bikinin dashboard admin modern dark mode dengan sidebar, chart, table, stats card')"><b>📊 Admin Dashboard</b><span>Sidebar collapsible, chart, kanban, dark modern</span></div>
<div class=t-card onclick="useT('Bikinin e-commerce product page modern dengan gallery, variant, cart, review')"><b>🛒 E-Commerce</b><span>Product gallery, variant, add to cart, review bintang</span></div>
</div><div style="margin-top:20px;padding:12px;background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.15);border-radius:12px;font-size:11px;color:var(--muted)">✨ Tips: Ketik "bikinin..." + klik Preview 👁️ buat lihat langsung jadi web!</div></div>`;}
function useT(t){document.getElementById('msg').value=t;autoGrow(document.getElementById('msg'));document.getElementById('msg').focus();}
function autoGrow(el){el.style.height='24px';el.style.height=el.scrollHeight+'px';}
function handleKey(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg();}}
function addCopy(){document.querySelectorAll('pre').forEach(pre=>{if(pre.querySelector('.copy-btn'))return;let b=document.createElement('button');b.className='copy-btn';b.textContent='Copy';b.onclick=()=>{navigator.clipboard.writeText(pre.querySelector('code')?.innerText||pre.innerText);b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1000)};pre.appendChild(b);})}
function extractHTML(text){let m=text.match(/```html([\\s\\S]*?)```/i);if(m)return m[1].trim();if(text.includes('<!DOCTYPE')||text.includes('<html')){let s=text.indexOf('<!DOCTYPE')!=-1?text.indexOf('<!DOCTYPE'):text.indexOf('<html');return text.slice(s, s+20000);}return null;}
function updatePreview(html){lastHTML=html;document.getElementById('previewFrame').srcdoc=html;document.getElementById('previewPanel').classList.add('open');}
function refreshPreview(){if(lastHTML)document.getElementById('previewFrame').srcdoc=lastHTML;}
function openCommand(){let cmd=prompt('⌘ Command Palette V7:\\n\\ngradient - bikin gradient\\nshadow - bikin shadow\\npalette - color palette\\nimage [prompt] - AI image gratis\\nseo - optimasi SEO\\nexport - export HTML\\n\\nKetik:');if(!cmd)return;toolAction(cmd.toLowerCase());}
function toolAction(type){
  if(type.includes('gradient')) sendDirect('Bikinin 5 gradient modern untuk web dark mode: aurora, mesh, linear untuk button & card, kasih CSS code + contoh pakai');
  else if(type.includes('shadow')) sendDirect('Bikinin koleksi box-shadow modern: soft, medium, dramatic, glow, glass - untuk card, button, modal - kasih CSS + contoh');
  else if(type.includes('palette')) sendDirect('Bikinin color palette lengkap untuk SaaS dark aurora: primary #8b5cf6, background, text, border, success, error - kasih hex + Tailwind config');
  else if(type.includes('image')){let p=type.replace('image','').trim()||prompt('Mau gambar apa?','modern saas dashboard dark aurora, minimal, 4k'); if(!p)return; let url=`https://image.pollinations.ai/prompt/${encodeURIComponent(p)}?width=1280&height=720&nologo=true&seed=${Math.floor(Math.random()*10000)}`; let ch=chats.find(c=>c.id===cur); ch.messages.push({role:'assistant',content:`![AI Generated](${url})\n\n**Prompt:** ${p}\n\n**URL buat dipakai:**\n\`\`\`html\n<img src="${url}" alt="${p}" />\n\`\`\`\n\nBisa langsung pakai di web lu!`}); renderC(); save();}
  else if(type.includes('seo')) sendDirect('Bikinin checklist SEO untuk landing page: title, meta description, OG tags, schema JSON-LD, heading structure, alt text, performance tips');
  else if(type.includes('export')) exportHTML();
}
function exportHTML(){if(!lastHTML) return alert('Belum ada HTML! Minta AI bikin web dulu, baru bisa export.'); let blob=new Blob([lastHTML],{type:'text/html'}); let a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=(chats.find(c=>c.id===cur)?.title||'yukio-web')+'.html'; a.click();}
function exportZip(){exportHTML(); alert('ZIP: Untuk V7 ini export HTML single file dulu. Kalau butuh ZIP dengan assets, bilang "bikinin web dengan assets terpisah" nanti gue bikinin!');}
function sendDirect(t){document.getElementById('msg').value=t; sendMsg();}
async function typeWriter(el, text){
  return new Promise(res=>{
    let i=0;function step(){
      if(i<text.length){
        let chunk=text.slice(0,i+40);
        try{el.innerHTML=marked.parse(chunk)+'<span class=cursor></span>'}catch{el.textContent=chunk}
        i+=40;document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;setTimeout(step,6);
      }else{el.innerHTML=marked.parse(text);el.querySelectorAll&&el.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));addCopy();let html=extractHTML(text);if(html){lastHTML=html;el.insertAdjacentHTML('beforeend',`<div class=msg-actions><button class="act primary" onclick="updatePreview(lastHTML)">👁️ Live Preview</button><button class=act onclick="navigator.clipboard.writeText(lastHTML);this.textContent='Copied!'">📋 Copy HTML</button><button class=act onclick="exportHTML()">📤 Export</button></div>`);}res();}
    }step();
  });
}
async function sendMsg(){
  let input=document.getElementById('msg');let t=input.value.trim();if(!t)return;
  let ch=chats.find(c=>c.id===cur);if(ch.messages.length===0)ch.title=t.slice(0,38);
  ch.messages.push({role:'user',content:t});input.value='';autoGrow(input);renderC();save();
  let div=document.createElement('div');div.className='msg';div.innerHTML=`<div class="avatar y">Y</div><div class=bubble><div class=content>⚡ Yukio Free AI ngetik<span class=cursor></span></div></div>`;
  document.getElementById('chatInner').appendChild(div);let contentEl=div.querySelector('.content');
  document.getElementById('send').disabled=true;
  try{let r=await fetch('/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:ch.messages.slice(-8)})});let j=await r.json();await typeWriter(contentEl,j.reply);ch.messages.push({role:'assistant',content:j.reply});save();}catch(e){contentEl.textContent='Error: '+e}
  document.getElementById('send').disabled=false;
}
function renderC(){let ch=chats.find(c=>c.id===cur);let inner=document.getElementById('chatInner');if(!ch){if(!chats.length)newChat();return;}if(ch.messages.length===0){renderW();return;}inner.innerHTML='';ch.messages.forEach(m=>{let d=document.createElement('div');d.className='msg';let html=m.role==='assistant'?extractHTML(m.content):null;let extra=html?`<div class=msg-actions><button class="act primary" onclick="updatePreview(lastHTML)">👁️ Preview</button><button class=act onclick="exportHTML()">📤 Export</button></div>`:'';d.innerHTML=`<div class="avatar ${m.role==='user'?'u':'y'}">${m.role==='user'?'U':'Y'}</div><div class=bubble><div class=content>${m.role==='user'?esc(m.content):marked.parse(m.content)}</div>${m.role==='assistant'?extra:''}</div>`;inner.appendChild(d);});inner.querySelectorAll('pre code').forEach(e=>hljs.highlightElement(e));addCopy();document.getElementById('chat').scrollTop=document.getElementById('chat').scrollHeight;}
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
            hist = data.get("history",[])[:6]
            if not msg:
                return jsonify({"reply":"Ketik dulu bos! Mau bikin web apa?"})

            # FREE AI - POLLINATIONS (TANPA TOKEN, ANTI CHAR 0)
            reply = None
            try:
                # Prompt builder untuk web builder
                system_prompt = """You are Yukio AI V7 - Ultimate Web Builder Expert. You are the best at creating modern websites.
                Rules:
                1. Always create FULL single-file HTML with inline CSS (no external CSS except Google Fonts)
                2. Style: dark aurora, glassmorphism, gradient, modern shadow, rounded 16-20px, Plus Jakarta Sans font
                3. Responsive, dark mode, smooth animation, hover effects
                4. For SaaS: hero with aurora, pricing 3 tier, testimonial, FAQ, CTA, footer
                5. Output must be ready to preview in iframe - complete HTML.
                6. Language: Indonesian santai for explanation, but code comments English.
                """
                # Gabung history biar nyambung
                hist_text = " ".join([f"{h.get('role')}: {h.get('content')[:300]}" for h in hist])[-800:]
                full_prompt = f"{system_prompt}\n\nContext: {hist_text}\n\nUser Request: {msg}\n\nCreate modern website. Output HTML in ```html code block:"
                
                encoded = urllib.parse.quote(full_prompt)
                # Random seed biar gak cache
                seed = random.randint(1,999999)
                # Pakai model openai (gratis & paling stabil di Pollinations)
                url = f"https://text.pollinations.ai/{encoded}?model=openai&seed={seed}&referrer=yukio-ai"
                
                r = requests.get(url, timeout=45, headers={"User-Agent":"YukioAI/7.0"})
                
                if r.status_code == 200 and r.text and len(r.text.strip()) > 20:
                    reply = r.text.strip()
                    # Kalau response kepotong gak ada closing html, tetep ok
                    if "<html" not in reply.lower() and "```html" not in reply.lower():
                        # Coba lagi dengan prompt lebih pendek kalau response aneh
                        if len(reply) < 100:
                            raise Exception("Response too short")
                else:
                    raise Exception(f"Status {r.status_code}: {r.text[:200]}")
                    
            except Exception as e:
                # Fallback 2: coba model mistral (free juga)
                try:
                    encoded2 = urllib.parse.quote(f"Bikinin website modern: {msg}. Kasih HTML lengkap single file dark aurora.")
                    r2 = requests.get(f"https://text.pollinations.ai/{encoded2}?model=mistral&seed={random.randint(1,9999)}", timeout=30)
                    if r2.status_code == 200 and len(r2.text) > 50:
                        reply = r2.text
                except:
                    pass

            # Final fallback - template siap pakai biar gak error kosong
            if not reply or len(reply.strip()) < 30:
                reply = f"""⚠️ AI gratis lagi rame bos, tapi gue kasih template SaaS dark aurora premium biar lu bisa langsung preview & edit:

```html
<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio SaaS - Dark Aurora</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}body{{font-family:'Plus Jakarta Sans',sans-serif;background:#06070d;color:#f8f8ff;overflow-x:hidden}}
.hero{{min-height:92vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 20px;background:radial-gradient(900px 500px at 20% -10%, rgba(139,92,246,.28), transparent),radial-gradient(800px 400px at 90% 10%, rgba(59,130,246,.18), transparent),radial-gradient(600px 300px at 50% 100%, rgba(6,255,165,.08), transparent)}}
.badge{{padding:8px 16px;background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.2);border-radius:20px;font-size:12px;color:#a78bfa;margin-bottom:20px}}
.hero h1{{font-size:clamp(32px,6vw,64px);font-weight:800;line-height:.95;letter-spacing:-.03em;background:linear-gradient(135deg,#fff 20%,#a78bfa 60%,#60a5fa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;max-width:800px}}
.hero p{{color:#9a9ab8;margin:20px auto 0;max-width:560px;font-size:16px;line-height:1.6}}
.btns{{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap;justify-content:center}}
.btn{{padding:14px 26px;border-radius:14px;font-weight:700;font-size:14px;cursor:pointer;border:none;transition:.2s}}.btn-primary{{background:linear-gradient(135deg,#8b5cf6,#3b82f6);color:#fff;box-shadow:0 10px 28px rgba(139,92,246,.35)}}.btn-ghost{{background:#151622;border:1px solid #23243a;color:#fff}}
.pricing{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;max-width:1100px;margin:80px auto;padding:0 20px}}
.card{{background:linear-gradient(180deg,#1c1d2f,#151622);border:1px solid #23243a;border-radius:20px;padding:28px;transition:.3s}}.card:hover{{transform:translateY(-4px);border-color:rgba(139,92,246,.3)}}.card.feat{{border-color:rgba(139,92,246,.5);background:linear-gradient(180deg,#1e1e35,#171728);box-shadow:0 20px 60px rgba(139,92,246,.15)}}.price{{font-size:36px;font-weight:800;margin:12px 0}}.feat-badge{{padding:4px 10px;background:linear-gradient(135deg,#8b5cf6,#3b82f6);border-radius:20px;font-size:10px;font-weight:700}}
.testi{{max-width:900px;margin:80px auto;padding:0 20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
.t{{background:#151622;border:1px solid #23243a;border-radius:16px;padding:20px;font-size:13px;color:#9a9ab8}}
</style></head><body>
<div class=hero><div class=badge>✨ V7 Free AI • Live Preview Ready</div><h1>Build Beautiful<br>Websites 10x Faster</h1><p>Yukio AI V7 pakai AI gratis 100% - bikin SaaS landing page, portfolio, dashboard modern dengan live preview & export 1 klik. Tanpa token, tanpa error.</p><div class=btns><button class="btn btn-primary">Start Building Free →</button><button class="btn btn-ghost">View Demo</button></div></div>
<div class=pricing>
<div class=card><h3>Starter</h3><div class=price>$29<span style="font-size:14px;color:#9a9ab8">/mo</span></div><p style="color:#9a9ab8;font-size:13px">Perfect for side projects & personal use</p><ul style="margin:16px 0;color:#9a9ab8;font-size:13px;line-height:2"><li>✓ 5 Projects</li><li>✓ Free AI Unlimited</li><li>✓ Live Preview</li></ul></div>
<div class="card feat"><div style="display:flex;justify-content:space-between;align-items:center"><h3>Pro</h3><span class=feat-badge>MOST POPULAR</span></div><div class=price>$79<span style="font-size:14px;color:#9a9ab8">/mo</span></div><p style="color:#9a9ab8;font-size:13px">Untuk startup & team yang serius</p><ul style="margin:16px 0;color:#9a9ab8;font-size:13px;line-height:2"><li>✓ Unlimited Projects</li><li>✓ All Web Tools</li><li>✓ Export ZIP + Deploy</li><li>✓ Priority Support</li></ul><button class="btn btn-primary" style="width:100%;margin-top:12px">Get Pro Now</button></div>
<div class=card><h3>Enterprise</h3><div class=price>$199<span style="font-size:14px;color:#9a9ab8">/mo</span></div><p style="color:#9a9ab8;font-size:13px">Untuk company besar & agency</p><ul style="margin:16px 0;color:#9a9ab8;font-size:13px;line-height:2"><li>✓ Everything in Pro</li><li>✓ White-label</li><li>✓ API Access</li></ul></div>
</div>
<div class=testi><div class=t>"Yukio V7 bikin landing page gue jadi kayak buatan designer $5000 dalam 5 detik!" - Andi, Founder SaaS</div><div class=t>"Live preview nya gila, langsung jadi web beneran, gak perlu coding!" - Sinta, Designer</div><div class=t>"Gratis selamanya tanpa token, ini yang gue cari!" - Budi, Developer</div></div>
<div style="text-align:center;padding:60px 20px;color:#9a9ab8;font-size:12px;border-top:1px solid #23243a;margin-top:40px">© 2026 Yukio AI V7 • Built with Free AI • Free Forever • No Token Needed</div>
</body></html>
