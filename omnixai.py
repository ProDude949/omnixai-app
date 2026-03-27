import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="OmnixAI", page_icon="🚀", layout="centered")

st.title("🚀 OmnixAI")
st.caption("Your Everything AI — Chat • Images • Videos")

# Sidebar
api_key = st.sidebar.text_input("🔑 xAI API Key", type="password", help="Get it from console.x.ai")

if not api_key:
    st.warning("Enter your xAI API key in the sidebar to start")
    st.stop()

client = OpenAI(base_url="https://api.x.ai/v1", api_key=api_key)

# Plan
if "plan" not in st.session_state:
    st.session_state.plan = "free"

plan_choice = st.sidebar.radio("Choose Plan", ["Free", "Pro ($12/month)"])
st.session_state.plan = "pro" if "Pro" in plan_choice else "free"

st.sidebar.caption("Free: Limited use\nPro: Unlimited + priority")

# Usage tracker
if "usage" not in st.session_state:
    st.session_state.usage = {"chat": 0, "img": 0, "vid": 0}

tab_chat, tab_img, tab_vid = st.tabs(["💬 Chat", "🖼️ Images", "🎥 Videos"])

# ====================== CHAT ======================
with tab_chat:
    st.subheader("Chat with OmnixAI")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Yo bro! I'm OmnixAI. Ask me anything — ideas, code, jokes, whatever 🔥"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me anything..."):
        if st.session_state.plan == "free" and st.session_state.usage["chat"] >= 20:
            st.error("Free limit reached (20 messages). Upgrade to Pro $12 for unlimited!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("OmnixAI thinking..."):
                response = client.chat.completions.create(
                    model="grok-4.20-0309-non-reasoning",   # ← Updated model
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                answer = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.usage["chat"] += 1

# ====================== IMAGES ======================
with tab_img:
    st.subheader("Generate Images (up to 13 free)")
    prompt = st.text_area("Describe the image", placeholder="Cyberpunk samurai cat in neon Tokyo rain")
    num = st.slider("Number of images", 1, 13 if st.session_state.plan == "free" else 20, 4)

    if st.button("🚀 Generate Images", type="primary"):
        if st.session_state.plan == "free" and st.session_state.usage["img"] + num > 13:
            st.error("Free limit: max 13 images")
        else:
            with st.spinner("Generating images..."):
                resp = client.images.generate(
                    model="grok-imagine-image",   # or check xAI for exact image model name
                    prompt=prompt,
                    n=num
                )
                cols = st.columns(3)
                for i, img in enumerate(resp.data):
                    with cols[i % 3]:
                        st.image(img.url, use_column_width=True)
            st.success("Done! Download quickly.")
            st.session_state.usage["img"] += num

# ====================== VIDEOS ======================
with tab_vid:
    st.subheader("Generate Short Videos (2 free)")
    vprompt = st.text_area("Describe the video", placeholder="Futuristic neon car drifting through cyber city")
    if st.button("🎬 Generate Video", type="primary"):
        if st.session_state.plan == "free" and st.session_state.usage["vid"] >= 2:
            st.error("Free limit: only 2 videos")
        else:
            st.info("Video generation is still rolling out on xAI. Chat + Images are working great for now!")
            st.session_state.usage["vid"] += 1   # placeholder

st.sidebar.divider()
st.sidebar.write(f"**Session Usage**")
st.sidebar.write(f"💬 Chat: {st.session_state.usage['chat']}")
st.sidebar.write(f"🖼️ Images: {st.session_state.usage['img']}")
st.sidebar.write(f"🎥 Videos: {st.session_state.usage['vid']}")
