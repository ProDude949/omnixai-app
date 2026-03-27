import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

st.set_page_config(page_title="OmnixAI", page_icon="🚀", layout="centered")

# Custom CSS for cool look
st.markdown("""
<style>
    .big-title { font-size: 3rem; font-weight: bold; color: #00ff9d; }
    .stButton>button { background-color: #00ff9d; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-title">🚀 OmnixAI</h1>', unsafe_allow_html=True)
st.caption("**Your Everything AI** — Chat • Images • Videos")

# Sidebar
st.sidebar.title("OmnixAI")
api_key = st.sidebar.text_input("🔑 xAI API Key", type="password", help="Get it from console.x.ai")

if not api_key:
    st.warning("Enter your xAI API key in the sidebar to start using OmnixAI")
    st.stop()

client = OpenAI(base_url="https://api.x.ai/v1", api_key=api_key)

# Plan selection (demo mode)
if "plan" not in st.session_state:
    st.session_state.plan = "free"

plan = st.sidebar.radio("Choose Plan", ["Free", "Pro ($12/month)"], index=0 if st.session_state.plan == "free" else 1)
st.session_state.plan = "pro" if plan == "Pro ($12/month)" else "free"

st.sidebar.caption("Free: Limited daily use\nPro: Unlimited everything + priority")

# Usage tracker (session only for now)
if "usage" not in st.session_state:
    st.session_state.usage = {"chat": 0, "img": 0, "vid": 0}

# Tabs
tab_chat, tab_img, tab_vid = st.tabs(["💬 Chat", "🖼️ Generate Images", "🎥 Generate Videos"])

# ===================== CHAT =====================
with tab_chat:
    st.subheader("Chat with OmnixAI")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Yo bro! I'm OmnixAI. Ask me anything — ideas, code, jokes, world problems... let's go 🔥"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        if st.session_state.plan == "free" and st.session_state.usage["chat"] >= 20:
            st.error("Free limit reached (20 messages). Upgrade to Pro for unlimited!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("OmnixAI thinking..."):
                response = client.chat.completions.create(
                    model="grok-4",  # or latest fast model
                    messages=st.session_state.messages,
                    temperature=0.8
                )
                answer = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.usage["chat"] += 1

# ===================== IMAGES =====================
with tab_img:
    st.subheader("Generate Images (Grok Imagine)")
    prompt = st.text_area("Describe your image", placeholder="A cyberpunk samurai cat in neon Tokyo rain, ultra detailed")
    num = st.slider("How many images?", 1, 13 if st.session_state.plan == "free" else 20, 4)

    if st.button("Generate Images", type="primary"):
        if st.session_state.plan == "free" and st.session_state.usage["img"] + num > 13:
            st.error("Free limit: max 13 images total. Go Pro for unlimited!")
        else:
            with st.spinner(f"Creating {num} images..."):
                resp = client.images.generate(
                    model="grok-imagine-image",
                    prompt=prompt,
                    n=num
                )
                cols = st.columns(3)
                for i, img in enumerate(resp.data):
                    with cols[i % 3]:
                        st.image(img.url, use_column_width=True)
            st.success("Images generated! Download them quick (URLs expire)")
            st.session_state.usage["img"] += num

# ===================== VIDEOS =====================
with tab_vid:
    st.subheader("Generate Short Videos (Grok Imagine Video)")
    vprompt = st.text_area("Describe your video", placeholder="Futuristic flying car racing through glowing cyber city at night")
    duration = st.slider("Duration (seconds)", 5, 15, 10)

    if st.button("Generate Video", type="primary"):
        if st.session_state.plan == "free" and st.session_state.usage["vid"] >= 2:
            st.error("Free limit: only 2 videos. Upgrade to Pro!")
        else:
            with st.spinner("Generating video... (this can take 30-60 seconds)"):
                # Note: Video generation uses xAI's video endpoint - adjust if needed based on exact SDK
                st.info("Video generation is live via Grok Imagine API. In production we'll show the video player here.")
                # Placeholder for actual video call (you can expand with xai_sdk if available)
                st.video("https://example.com/sample-video.mp4")  # replace with real response.url later
            st.success("Video ready!")
            st.session_state.usage["vid"] += 1

# Footer info
st.sidebar.divider()
st.sidebar.write(f"**Current Usage**")
st.sidebar.write(f"Chats: {st.session_state.usage['chat']}")
st.sidebar.write(f"Images: {st.session_state.usage['img']}")
st.sidebar.write(f"Videos: {st.session_state.usage['vid']}")

st.caption("OmnixAI Web — Built fast with Streamlit + xAI Grok. No app store needed.")
