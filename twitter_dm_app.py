import os
import tweepy
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
)

def check_connection():
    try:
        me = client.get_me()
        if me.data:
            return f"CONNECTED: @{me.data.username}"
        return "CONNECTION FAILED"
    except Exception as e:
        return f"ERROR: {str(e)[:40]}"

CONNECTED_STATUS = check_connection()
print(CONNECTED_STATUS)

def get_user_id(username):
    username = username.lstrip("@").strip()
    try:
        res = client.get_user(username=username)
        if res.data:
            return str(res.data.id)
    except Exception as e:
        print(f"[get_user_id] {e}")
    return None

def send_dm(recipient_id, message):
    try:
        res = client.create_direct_message(
            participant_id=int(recipient_id),
            text=message,
            user_auth=True,
        )
        return {"success": True, "data": res.data}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_send(username, message):
    if not username or not username.strip():
        return "[ERROR] NO USERNAME PROVIDED"
    if not message or not message.strip():
        return "[ERROR] NO MESSAGE PROVIDED"

    clean = username.lstrip("@").strip()
    user_id = get_user_id(clean)

    if user_id is None:
        return f'[ERROR] USER @{clean} NOT FOUND'

    result = send_dm(user_id, message.strip())

    if result["success"]:
        return f'MESSAGE SENT\nTO: @{clean}\nUSER_ID: {user_id}\nCONTENT: "{message.strip()}"'
    return f'[FAILED] {result["error"]}'

CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

* {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
}

body {
    background: #0a0a0a;
}

.gradio-container {
    max-width: 680px !important;
    margin: 0 auto !important;
}

.main-box {
    background: #111;
    border: 2px solid #333;
    padding: 0;
    margin: 40px 0;
}

.header-bar {
    background: #1a1a1a;
    border-bottom: 2px solid #333;
    padding: 16px 24px;
}

.header-bar h1 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.status-bar {
    background: #0d0d0d;
    border-bottom: 1px solid #222;
    padding: 10px 24px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
}

.status-bar.ok {
    color: #00ff00;
}

.status-bar.err {
    color: #ff0000;
}

.content-area {
    padding: 32px 24px;
}

.field-wrapper {
    margin-bottom: 24px;
}

.field-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

input, textarea {
    width: 100%;
    padding: 12px 14px;
    background: #0d0d0d;
    border: 1px solid #333;
    color: #fff;
    font-size: 0.9rem;
    transition: all 0.2s;
}

input:focus, textarea:focus {
    outline: none;
    border-color: #666;
    background: #151515;
}

input::placeholder, textarea::placeholder {
    color: #444;
}

textarea {
    resize: vertical;
    min-height: 120px;
    font-family: 'JetBrains Mono', monospace;
}

.btn-container {
    margin-top: 28px;
    display: flex;
    justify-content: flex-end;
}

button {
    padding: 12px 32px;
    background: #fff;
    color: #000;
    border: none;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    cursor: pointer;
    transition: all 0.15s;
}

button:hover {
    background: #e0e0e0;
}

button:active {
    background: #c0c0c0;
}

.output-terminal {
    margin-top: 24px;
    padding: 16px;
    background: #000;
    border: 1px solid #333;
    color: #0f0;
    font-size: 0.85rem;
    min-height: 60px;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
}

.footer-bar {
    background: #0d0d0d;
    border-top: 1px solid #222;
    padding: 12px 24px;
    font-size: 0.7rem;
    color: #555;
    text-align: right;
    letter-spacing: 1px;
}
"""

def build():
    with gr.Blocks(css=CSS) as demo:
        with gr.Column(elem_classes="main-box"):
            gr.HTML('<div class="header-bar"><h1>Twitter DM</h1></div>')
            
            if "CONNECTED" in CONNECTED_STATUS:
                gr.HTML(f'<div class="status-bar ok">{CONNECTED_STATUS}</div>')
            else:
                gr.HTML(f'<div class="status-bar err">{CONNECTED_STATUS}</div>')
            
            with gr.Column(elem_classes="content-area"):
                gr.HTML('<div class="field-wrapper"><span class="field-label">Target Username</span></div>')
                username = gr.Textbox(placeholder="e.g. elonmusk", container=False, show_label=False)
                
                gr.HTML('<div class="field-wrapper" style="margin-top:24px;"><span class="field-label">Message Content</span></div>')
                message = gr.Textbox(placeholder="message text", lines=5, container=False, show_label=False)
                
                with gr.Row(elem_classes="btn-container"):
                    btn = gr.Button("SEND")
                
                status = gr.Textbox(
                    value="[SYSTEM READY]",
                    interactive=False,
                    show_label=False,
                    container=False,
                    elem_classes="output-terminal"
                )
            
            gr.HTML('<div class="footer-bar">TWEEPY v4.14.0 / GRADIO</div>')
            
            btn.click(fn=handle_send, inputs=[username, message], outputs=[status])
    
    return demo

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    print(f"INITIALIZING → PORT {port}")
    build().launch(server_name="0.0.0.0", server_port=port, share=False)