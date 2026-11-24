from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from src.generator import build_prompt, count_spoken_characters, extract_spoken_script

load_dotenv()

st.set_page_config(
    page_title="TikTok Scripts Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
  background: radial-gradient(ellipse at 80% 0%, #25204c 0%, #111321 42%, #0a0b12 100%);
}
.block-container { max-width: 1100px; padding-top: 2rem; }
.hero {
  padding: 1.7rem 1.8rem; border: 1px solid #38365c; border-radius: 20px;
  background: linear-gradient(120deg, rgba(25,28,53,.96), rgba(43,31,80,.92));
  margin-bottom: 1.2rem;
}
.hero h1 { margin: 0; font-size: clamp(2rem, 4vw, 3rem); letter-spacing: -.04em; }
.hero p { color: #c6c8e2; margin: .45rem 0 0; font-size: 1.05rem; }
div[data-testid="stMetric"] {
  background: rgba(255,255,255,.035); border: 1px solid #343650;
  padding: 12px 16px; border-radius: 14px;
}
div.stButton > button, div.stDownloadButton > button { border-radius: 10px; font-weight: 650; }
[data-testid="stSidebar"] { background: rgba(13,15,28,.92); }
.muted { color: #aeb1cc; font-size: .9rem; }
</style>
<div class="hero">
  <h1>🎬 TikTok Scripts Generator</h1>
  <p>Turn a video idea into a ready-to-record short-form script.</p>
</div>
""", unsafe_allow_html=True)

LANGUAGES = ["English", "Russian", "Spanish", "German", "French", "Italian", "Portuguese"]
TONES = [
    "Confident and punchy", "Funny and playful", "Educational and clear",
    "Storytelling", "Bold and provocative (not misleading)", "Calm and friendly",
    "Documentary", "Personal and relatable",
]
NICHES = [
    "Personal growth", "Confidence and social skills", "Lifestyle and habits",
    "Education", "Technology and AI", "Fitness and wellbeing",
    "Relationships", "Business and money", "Gaming", "Beauty and fashion",
    "Food and cooking", "Travel", "Other",
]

with st.sidebar:
    st.header("⚙️ Script settings")
    language = st.selectbox("Output language", LANGUAGES, index=0)
    tone = st.selectbox("Tone", TONES, index=0)
    niche = st.selectbox("Content niche", NICHES, index=0)
    duration = st.select_slider(
        "Target video length",
        options=[15, 20, 30, 35, 40, 45, 60, 90],
        value=35,
        format_func=lambda n: f"{n} seconds",
    )
    max_chars = st.slider("Spoken-script character limit", 100, 1600, 500, 50)
    st.divider()
    include_cta = st.checkbox("Include a call to action", value=True)
    include_shots = st.checkbox("Include a shot list", value=True)
    include_captions = st.checkbox("Include on-screen captions", value=True)
    include_hashtags = st.checkbox("Suggest hashtags", value=True)
    st.caption("The spoken script is kept separate from production notes.")

left, right = st.columns([1.25, 0.75], gap="large")
with left:
    st.subheader("1. Describe your video")
    with st.form("script_form"):
        topic = st.text_input(
            "Video topic",
            placeholder="e.g. 3 small habits that make you more confident",
        )
        audience = st.text_input("Target audience", value="Young adults aged 18–30")
        platform = st.selectbox("Platform", ["TikTok", "Instagram Reels", "YouTube Shorts", "All short-form platforms"])
        key_message = st.text_area(
            "Key point or takeaway (optional)",
            placeholder="What should viewers remember?",
            height=90,
        )
        extra = st.text_area(
            "Extra instructions (optional)",
            placeholder="Facts to include, phrases to avoid, personal angle, etc.",
            height=90,
        )
        submitted = st.form_submit_button("✨ Generate script", type="primary", use_container_width=True)

with right:
    st.subheader("2. Generation notes")
    st.markdown(
        f"""
        **Your settings**
        - Language: {language}
        - Style: {tone}
        - Length: {duration} seconds
        - Max spoken characters: {max_chars}
        """
    )
    st.info(
        "A strong opening, one clear idea, and a specific payoff usually work better "
        "than stuffing a short video with too many points."
    )
    st.markdown('<p class="muted">You can review, edit, and download the generated result below.</p>', unsafe_allow_html=True)

def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        try:
            key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
        except Exception:
            key = ""
    return key

if submitted:
    if not topic.strip():
        st.error("Please enter a video topic.")
    else:
        api_key = get_api_key()
        if not api_key:
            st.error(
                "No API key found. Set OPENAI_API_KEY in your environment or Streamlit Secrets. "
                "See the README for setup instructions."
            )
        else:
            prompt = build_prompt(
                topic=topic.strip(),
                audience=audience.strip() or "General audience",
                platform=platform,
                niche=niche,
                language=language,
                tone=tone,
                duration_seconds=duration,
                max_characters=max_chars,
                key_message=key_message.strip(),
                extra_instructions=extra.strip(),
                include_cta=include_cta,
                include_shot_list=include_shots,
                include_captions=include_captions,
                include_hashtags=include_hashtags,
            )
            try:
                with st.spinner("Writing and polishing your script..."):
                    client = OpenAI(api_key=api_key)
                    response = client.responses.create(
                        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                        input=prompt,
                    )
                    result = response.output_text.strip()
                st.session_state["latest_script"] = result
                st.session_state["latest_topic"] = topic.strip()
                st.session_state["latest_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                st.caption("Check your API key, account access, and network connection.")

if "latest_script" in st.session_state:
    st.divider()
    st.subheader("3. Your script")
    script = st.session_state["latest_script"]
    spoken = extract_spoken_script(script)
    char_count = count_spoken_characters(spoken)
    m1, m2, m3 = st.columns(3)
    m1.metric("Spoken characters", f"{char_count:,}")
    m2.metric("Target length", f"{duration} sec")
    m3.metric("Generated", st.session_state.get("latest_time", "Just now"))
    if char_count > max_chars:
        st.warning(f"The generated spoken script is over your {max_chars}-character target. Edit it before recording.")
    st.text_area("Editable output", value=script, height=440, key="editable_output")
    final_text = st.session_state.get("editable_output", script)
    st.download_button(
        "⬇️ Download script (.txt)",
        data=final_text,
        file_name="tiktok-script.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.download_button(
        "⬇️ Download script (.md)",
        data=final_text,
        file_name="tiktok-script.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.caption("Review factual claims, music rights, and platform rules before publishing.")

with st.expander("🔐 Privacy and API usage"):
    st.write(
        "This app sends your prompt to the AI provider using your API key. Do not include passwords, "
        "private personal information, or confidential business data. API usage may incur charges "
        "depending on your provider and account. This app does not store a server-side script history."
    )

st.divider()
st.caption("Open-source creator tool · Built with Python and Streamlit")
