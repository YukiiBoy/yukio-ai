from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

JUICE_KEY = os.environ.get("JUICE_KEY")
API_URL = "https://api.tokenjuice.ai/v1/chat/completions"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Yukio AI - V4.1 Flash</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Inter,system-ui,sans-serif}
body{display:flex;height:100vh;background:#0f0f0f;color:#ececec;overflow:hidden}
#sidebar{width:260px;background:#171717;display:flex;flex-direction:column;padding:10px}
#newchat{background:#2f2f2f;border:none;color:#fff;padding:12px;border-radius:10px;cursor:pointer;margin:8px 0;font-weight:600}
#history{flex:1;overflow-y:auto;margin-top:10px}
.chat-item{padding:10px;border-radius:8px;cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:14px;color:#aaa}
.chat-item:hover,.chat-item.active{background:#2f2f2f;color:#fff}
#main{flex:1;display:flex;flex-direction:column;background:#212121}
#chat{flex:1;overflow-y:auto;padding:20px;max-width:800px;width:100%;margin:0 auto}
.msg{display:flex;gap:12px;margin:18px 0;line-height:1.6}
.avatar{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0}
.u{background:#fff;color:#000}.y{background:#4a9eff;color:#fff}
.bubble{flex:1;overflow-x:auto}.bubble pre{background:#0d0d0d;padding:14px;border-radius:10px;overflow-x:auto;margin:10px 0}
#inputBox{padding:16px;max-width:800px;width:100%;margin:0 auto}
#inputWrap{background:#2f2f2f;border-radius:24px;display:flex;align-items:center;padding:6px 12px}
#msg{flex:1;background:transparent;border:none;color:#fff;padding:12px;outline:none;font-size:15px}
#send{width:32px;height:32px;border-radius:50%;border:none;background:#fff;cursor:pointer;font-weight:700}
</style>
</head>
<body>
<div id="sidebar"><h2 style="padding:12px 8px">Yukio AI ⚡ V4.1</h2><button id="newchat" onclick="newChat()">+ New Chat</button><div id="history"></div></div>
<div id="main"><div id="chat"></div><div id="inputBox"><div id="inputWrap"><input id="msg" placeholder="Tanya apa aja ke Yukio AI V4.1 Flash..." onkeydown="if(event.key==='Enter')sendMsg()"><button id="send" onclick="sendMsg()">↑</button></div></div></div>
<script>
let chats = JSON.parse(localStorage.getItem('yukio_chats')||'[]');
let currentId = localStorage.getItem('yukio_current')||null;
function save(){localStorage.setItem('yukio_chats',JSON.stringify(chats));localStorage.setItem('yukio_current',currentId);renderHistory()}
function newChat(){currentId=Date.now().toString();chats.unshift({id:currentId,title:'New Chat',messages:[{role:'assistant',content:'Halo bos! Gue Yukio AI V4.1 Flash ⚡ Lebih cepat & pinter! Mau bikin bot discord toko? Gas!'}]});save();renderChat();}
function renderHistory(){let h=document.getElementById('history');h.innerHTML='';chats.forEach(c=>{let d=document.createElement('div');d.className='chat-item'+(c.id===currentId?' active':'');d.textContent=c.title;d.onclick=()=>{currentId=c.id;save();renderChat()};h.appendChild(d);});}
function renderChat(){let chat=chats.find(c=>c.id===currentId);if(!chat){if(chats.length===0)newChat();return;}let box=document.getElementById('chat');box.innerHTML='';chat.messages.forEach(m=>{let div=document.createElement('div');div.className='msg';let av=document.createElement('div');av.className='avatar '+(m.role==='user'?'u':'y');av.textContent=m.role==='user'?'U':'Y';let bub=document.createElement('div');bub.className='bubble';if(m.role==='user')bub.textContent=m.content;else bub.innerHTML=marked.parse(m.content);div.appendChild(av);div.appendChild(bub);box.appendChild(div);});box.querySelectorAll('pre code').forEach(el=>hljs.highlightElement(el));box.scrollTop=box.scrollHeight;}
async function sendMsg(){let input=document.getElementById('msg');let text=input.value.trim();if(!text)return;let chat=chats.find(c=>c.id===currentId);if(chat.messages.length===1)chat.title=text.slice(0,30);chat.messages.push({role:'user',content:text});input.value='';renderChat();save();chat.messages.push({role:'assistant',content:'_Yukio V4.1 lagi mikir..._'});renderChat();try{let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});let data=await res.json();chat.messages[chat.messages.length-1].content=data.reply||'Error: reply kosong';}catch(e){chat.messages[chat.messages.length-1].content='Error: '+e}renderChat();save();}
if(chats.length===0)newChat();else{renderHistory();renderChat();}renderHistory();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return HTML_PAGE

@app.route("/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json(silent=True) or {}
        user_msg = body.get("message", "")
        if not user_msg.strip():
            return jsonify({"reply": "Ketik dulu bos!"})

        headers = {"Authorization": f"Bearer {JUICE_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V4.1-Flash-1017",
            "messages": [
                {"role": "system", "content": "Kamu adalah Yukio AI V4.1 Flash, asisten coding handal buatan Yukioshop. Jawab langsung to the point, kasih kode lengkap pakai markdown."},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        r = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        if r.status_code != 200:
            return jsonify({"reply": f"Error TokenJuice {r.status_code}: {r.text[:800]}"})

        j = r.json()
        choice = j.get("choices", [{}])[0]
        message = choice.get("message", {})
        reply = message.get("content") or message.get("reasoning_content") or ""
        
        if not reply:
            reply = f"Respon kosong bos. Raw: {str(j)[:1000]}"
            
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error server: {e}"})
