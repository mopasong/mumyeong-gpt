import streamlit as st
import time
import json
from datetime import datetime
from input_collector import InputCollector
from prompt_generator import generate_prompt

st.set_page_config(page_title="🧠 Mumyeong GPT Prototype", layout="centered")
st.markdown("<style>div[data-testid='stTextArea'] textarea {font-family: 'Courier New'; font-size: 14px;}</style>", unsafe_allow_html=True)

collector = InputCollector()

st.title("🧠 Mumyeong GPT Prototype")
st.write("철학 기반 AI: 해석하지 않고, 기억하고, 존재하는...")

if "log" not in st.session_state:
    st.session_state.log = []

user_input = st.text_input("💬 Say something...", key="user_input")

if user_input:
    entry = collector.collect(user_input)
    st.session_state.log.append(entry)

    # Detect loop (mock rule: same phrase used multiple times)
    texts = [e["text"] for e in st.session_state.log]
    loop_detected = texts.count(user_input) > 1

    # Avoidance detection (mock rule: 포함된 회피 단어)
    avoidance_keywords = ["괜찮", "그냥", "몰라", "다 그래", "비슷"]
    is_avoidance = any(word in user_input for word in avoidance_keywords)

    # Visual feedback
    if entry["delay_since_last"] > 5:
        st.markdown("<div style='background-color:#ddd; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown("<div style='color:#888;'>🤫 침묵이 감지되었습니다.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size: 24px;'>● ● ●</div>", unsafe_allow_html=True)

    if loop_detected:
        st.warning("🔁 반복된 흐름이 감지되었습니다.")
    if is_avoidance:
        st.info("🌀 회피형 표현이 감지되었습니다.")

    # Prompt
    prompt = generate_prompt(st.session_state.log)
    st.markdown("#### ✍️ 생성된 GPT 프롬프트")
    st.code(prompt, language="markdown")

    # Mock GPT response (for demo)
    st.markdown("#### 🤖 AI의 응답")
    st.success("...이 흐름, 익숙하네요. 하지만 이번에는 조금 다르게 느껴집니다.")

# --- Save log to JSON and allow download ---
if st.session_state.log:
    if st.button("📥 대화 기록 저장하기 (JSON)"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mumyeong_log_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(st.session_state.log, f, ensure_ascii=False, indent=2)
        with open(filename, "rb") as f:
            st.download_button("⬇️ 다운로드", data=f, file_name=filename, mime="application/json")
