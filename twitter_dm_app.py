import os
import tweepy
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

# =============================
# Twitter Client
# =============================
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
            return f"@{me.data.username}"
        return "Not Connected"
    except Exception:
        return "Connection Error"

CONNECTED_STATUS = check_connection()
print(f"Status: {CONNECTED_STATUS}")

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
        client.create_direct_message(
            participant_id=int(recipient_id),
            text=message,
            user_auth=True,
        )
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_send(username, message):
    if not username or not username.strip():
        return "❌ Username is required"
    if not message or not message.strip():
        return "❌ Message cannot be empty"

    clean = username.lstrip("@").strip()
    user_id = get_user_id(clean)

    if user_id is None:
        return f"❌ User @{clean} not found"

    result = send_dm(user_id, message.strip())

    if result["success"]:
        return (
            f"✅ Message sent successfully\n\n"
            f"User: @{clean}\n"
            f"User ID: {user_id}\n\n"
            f"Message:\n{message.strip()}"
        )

    return f"❌ Failed to send message\n\n{result['error']}"

# =============================
# INTERNAL TOOL CSS
# =============================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

body {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%) !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide Gradio Footer */
footer {
    display: none !important;
}

.gradio-container footer {
    display: none !important;
}

/* Top Bar */
.top-bar {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    padding: 24px 40px;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
    position: relative;
    overflow: hidden;
}

.top-bar::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
    pointer-events: none;
}

.top-bar h1 {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
    position: relative;
    z-index: 1;
}

.connection-info {
    margin-top: 8px;
    font-size: 14px;
    color: rgba(255,255,255,0.9);
    font-weight: 500;
    position: relative;
    z-index: 1;
}

.connection-info::before {
    content: '●';
    color: #34d399;
    margin-right: 8px;
    font-size: 12px;
}

/* Main Container */
.main-wrapper {
    max-width: 800px;
    margin: 56px auto;
    padding: 0 32px;
}

/* Card */
.card {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.04);
    padding: 32px 36px;
    margin-bottom: 24px;
    border: 1px solid rgba(99, 102, 241, 0.08);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 12px 32px rgba(0,0,0,0.06);
    transform: translateY(-2px);
}

.card-title {
    font-size: 13px;
    font-weight: 700;
    color: #6366f1;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-title::before {
    content: '';
    width: 4px;
    height: 16px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 2px;
}

/* Input Fields */
label {
    display: block !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #1e293b !important;
    margin-bottom: 10px !important;
}

input[type="text"], 
textarea {
    width: 100% !important;
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    color: #0f172a !important;
    line-height: 1.5 !important;
    transition: all 0.2s ease !important;
}

input[type="text"]::placeholder,
textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}

input[type="text"]:hover,
textarea:hover {
    border-color: #cbd5e1 !important;
}

input[type="text"]:focus, 
textarea:focus {
    outline: none !important;
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1) !important;
    background: #fafafa !important;
}

textarea {
    min-height: 200px !important;
    resize: vertical !important;
    font-family: 'Inter', sans-serif !important;
}

/* Button */
.button-wrapper {
    margin-top: 32px;
    display: flex;
    justify-content: flex-start;
}

button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 32px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    letter-spacing: 0.3px !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
}

button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3) !important;
}

/* Status Display */
.status-box {
    margin-top: 32px;
    padding: 20px 24px;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    font-size: 14px;
    color: #334155;
    line-height: 1.7;
    white-space: pre-wrap;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Remove Gradio defaults */
.gradio-container .wrap,
.gradio-container .form,
.gradio-container .block {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.gradio-container .gap {
    gap: 0 !important;
}

/* Extra polish */
::selection {
    background: rgba(99, 102, 241, 0.2);
    color: #1e293b;
}
"""

# =============================
# UI BUILD
# =============================
def build():
    with gr.Blocks(title="Twitter DM Tool") as demo:
        
        # Header
        gr.HTML(f"""
            <div class="top-bar">
                <h1>Twitter Direct Message Tool</h1>
                <div class="connection-info">Connected as {CONNECTED_STATUS}</div>
            </div>
        """)
        
        # Main Content
        with gr.Column(elem_classes="main-wrapper"):
            
            # Recipient Card
            gr.HTML('<div class="card"><div class="card-title">Recipient</div>')
            username = gr.Textbox(
                label="Twitter Username",
                placeholder="elonmusk",
                container=False,
            )
            gr.HTML('</div>')
            
            # Message Card
            gr.HTML('<div class="card"><div class="card-title">Message</div>')
            message = gr.Textbox(
                label="Message Body",
                placeholder="Write your message here...",
                lines=7,
                container=False,
            )
            gr.HTML('</div>')
            
            # Button
            gr.HTML('<div class="button-wrapper">')
            send_btn = gr.Button("Send Message", variant="primary", size="lg")
            gr.HTML('</div>')
            
            # Status
            status = gr.Markdown(
                value="Ready to send",
                elem_classes="status-box",
            )
        
        # Events
        send_btn.click(handle_send, [username, message], status)
    
    return demo

# =============================
# ENTRY POINT
# =============================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    print(f"Starting on port {port}")
    build().launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        css=CSS,
    )
