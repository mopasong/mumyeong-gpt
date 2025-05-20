import streamlit as st
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

from input_collector import InputCollector
from prompt_generator import generate_prompt
from ai_connector import call_huggingface_api
from structure_graph import draw_structure_graph

st.set_page_config(page_title="🧠 Mumyeong GPT Prototype", layout="centered")
collector = InputCollector()

if "log" not in st.session_state:
    st.session_state.log = []

# Group input by date
def group_by_day(log):
    result = defaultdict(list)
    for entry in log:
        dt = datetime.fromtimestamp(entry["timestamp"])
        day_key = dt.strftime("%Y-%m-%d")
        result[day_key].append(entry)
    return result

# Emotion color mapping
def get_color_by_emotion(text):
    if any(k in text for k in ["무서워", "싫어", "두려워"]):
        return "#6c5ce7"
    if any(k in text for k in ["그냥", "몰라", "비슷"]):
        return "#b2bec3"
    if any(k in text for k in ["화나", "짜증", "폭발"]):
        return "#d63031"
    if any(k in text for k in ["좋아", "고마워", "다행"]):
        return "#00cec9"
    return "#ffeaa7"

# CSS animations
st.markdown("""
    <style>
    @keyframes fadeDots {
        0% {opacity: 1;}
        50% {opacity: 0.3;}
        100% {opacity: 0;}
    }
    .dot-anim {
        font-size: 30px;
        color: #ffeaa7;
        animation: fadeDots 3s ease-in-out infinite;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Mumyeong GPT Prototype")

# Input field
user_input = st.text_input("💬 Say something...", key="user_input")
huggingface_token = st.text_input("🔐 HuggingFace API Token (hf_...)", type="password")

if user_input:
    entry = collector.collect(user_input)
    st.session_state.log.append(entry)

    delay = entry["delay_since_last"]
    color = get_color_by_emotion(user_input)

    if delay > 5:
        st.markdown(f"<div style='height:50px; background-color:#dfe6e9;'></div>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown("<div style='color:#636e72;'>🤫 침묵이 감지되었습니다.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='dot-anim' style='color:{color}'>● ● ●</div>", unsafe_allow_html=True)

    # Detection
    texts = [e["text"] for e in st.session_state.log]
    if texts.count(user_input) > 1:
        st.warning("🔁 반복된 흐름이 감지되었습니다.")
    if any(word in user_input for word in ["괜찮", "그냥", "몰라", "비슷"]):
        st.info("🌀 회피형 표현이 감지되었습니다.")

    # Prompt + GPT response
    prompt = generate_prompt(st.session_state.log)
    st.markdown("#### ✍️ GPT 프롬프트")
    st.code(prompt, language="markdown")

    if huggingface_token.startswith("hf_"):
        with st.spinner("🤖 AI 응답 생성 중..."):
            ai_reply = call_huggingface_api(prompt, huggingface_token)
        st.markdown("#### 🤖 HuggingFace AI 응답")
        st.success(ai_reply)
    else:
        st.warning("❗ HuggingFace API 토큰을 입력해 주세요.")

# 📈 Timeline visualization
if st.session_state.log:
    st.markdown("### 📊 일자별 입력 수")
    grouped = group_by_day(st.session_state.log)
    days = list(grouped.keys())
    counts = [len(grouped[day]) for day in days]
    fig, ax = plt.subplots()
    ax.plot(days, counts, marker='o', color='#00b894')
    ax.set_ylabel("입력 횟수")
    ax.set_title("시간 흐름 속 입력 변화")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🧠 Day 30 구조 분석
if len(set(group_by_day(st.session_state.log).keys())) >= 30:
    st.markdown("### 🧠 Day 30 구조 발화")
    st.info("너의 30일 흐름은 반복과 침묵이 주기적으로 나타나고 있어요. 그 안에 익숙함과 회피가 공존했어.")

# 🕸 구조 노드 그래프 시각화
if st.session_state.log:
    st.markdown("### 🕸 구조 흐름 그래프")
    draw_structure_graph(st.session_state.log)

# 📥 저장
if st.session_state.log:
    if st.button("📤 JSON 저장"):
        filename = f"mumyeong_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(st.session_state.log, f, ensure_ascii=False, indent=2)
        with open(filename, "rb") as f:
            st.download_button("⬇️ 다운로드", data=f, file_name=filename, mime="application/json")
