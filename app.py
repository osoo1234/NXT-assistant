import streamlit as st
import google.generativeai as genai
from PIL import Image
import os, base64
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("ضع مفتاح GEMINI_API_KEY في ملف .env")
    st.stop()
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="NXT assistant", page_icon="🤖", layout="wide")

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_base64 = get_base64("space_bg.jpg")

st.markdown(f"""
<style>
@keyframes fadeInDown {{
    0% {{opacity: 0; transform: translateY(-30px);}}
    100% {{opacity: 1; transform: translateY(0);}}
}}
@keyframes fadeInUp {{
    0% {{opacity: 0; transform: translateY(30px);}}
    100% {{opacity: 1; transform: translateY(0);}}
}}
@keyframes fadeInBubbleUser {{
    0% {{opacity: 0; transform: translateX(30px);}}
    100% {{opacity: 1; transform: translateX(0);}}
}}
@keyframes fadeInBubbleBot {{
    0% {{opacity: 0; transform: translateX(-30px);}}
    100% {{opacity: 1; transform: translateX(0);}}
}}
.stApp {{
    background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed;
    background-size: cover;
}}
.logo-anim {{
    animation: fadeInDown 1s ease-out;
    text-align: center;
}}
.title-anim {{
    animation: fadeInUp 1.2s ease-out;
    text-align: center;
}}
.user-bubble {{
    animation: fadeInBubbleUser 0.4s ease-out;
}}
.bot-bubble {{
    animation: fadeInBubbleBot 0.4s ease-out;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='logo-anim' style="display: flex; justify-content: center; align-items: center;">
        <img src="data:image/png;base64,{get_base64('logo.png')}" width="200">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<h2 class='title-anim' style='color: white;'>💬 NXT assistant</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble' style='text-align: right; background-color: rgba(0,0,0,0.5); padding:10px; border-radius:10px; margin:5px; color:white;'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble' style='text-align: left; background-color: rgba(255,255,255,0.8); padding:10px; border-radius:10px; margin:5px; color:black;'>{msg['content']}</div>", unsafe_allow_html=True)

def send_message():
    user_msg = st.session_state.chat_input.strip()
    if not user_msg:
        return
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.chat_input = ""
    low_msg = user_msg.lower()
    if any(q in low_msg for q in ["اسمك", "انت مين", "مين انت", "what is your name", "who are you", "your name", "ur name"]):
        reply = "أنا اسمي نكست، صممتني مؤسسة Amazing Ai."
    elif any(q in low_msg for q in ["amazing ai", "amazingai", "اميزينج", "اميزنج", "امازينج", "ايه هي اميزينج", "ما هي اميزينج"]):
        reply = "Amazing Ai - AI beyond limits."
    else:
        history = [{"role": "user", "parts": [{"text": m["content"]}]} if m["role"] == "user" else {"role": "model", "parts": [{"text": m["content"]}]} for m in st.session_state.messages]
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(history)
        reply = resp.text.strip() if resp and resp.text else "حصل خطأ."
    st.session_state.messages.append({"role": "assistant", "content": reply})
st.text_input("أدخل رسالتك هنا:", key="chat_input", on_change=send_message)
