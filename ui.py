import streamlit as st
import time
from input_collector import InputCollector
from prompt_generator import generate_prompt

st.set_page_config(page_title="Mumyeong GPT Prototype", layout="centered")

collector = InputCollector()

st.title("🧠 Mumyeong GPT Prototype")
user_input = st.text_input("Say something...", key="input")

if user_input:
    entry = collector.collect(user_input)

    # 시각적 반응 시뮬레이션
    if entry["delay_since_last"] > 5:
        st.markdown("<div style='background-color:gray; height:50px; border-radius:10px;'> </div>", unsafe_allow_html=True)
        time.sleep(1)
        st.markdown("<div style='color:#888;'>[침묵이 감지되었습니다]</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='animation: blink 1s infinite;'>●●●</div>", unsafe_allow_html=True)

    prompt = generate_prompt(collector.log)
    st.text_area("📜 GPT Prompt", prompt, height=300)