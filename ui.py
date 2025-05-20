import streamlit as st
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
from input_collector import InputCollector
from prompt_generator import generate_prompt

st.set_page_config(page_title="🧠 Mumyeong GPT Prototype", layout="centered")

st.markdown("<style>div[data-testid='stTextArea'] textarea {font-family: 'Courier New'; font-size: 14px;}</style>", unsafe_allow_html=True)

collector = InputCollector()
if "log" not in st.session_state:
    st.session_state.log = []

# 기록 구조 (Day 기준 분류)
def group_by_day(log):
    result = {}
    for entry in log:
        dt = datetime.fromtimestamp(entry["timestamp"])
        day_key = dt.strftime("Day %Y-%m-%d")
        if day_key not in result:
            result[day_key] = []
        result[day_key].append(entry)
    return result

# 감각 기반 색상 매핑
def get_color_by_emotion(text):
    if any(k in text for k in ["무서워", "싫어", "두려워"]):
        return "#6c5ce7"  # 보라
    if any(k in text for k in ["그냥", "몰라", "비슷"]):
        return "#b2bec3"  # 회색
    if any(k in text for k in ["화나", "짜증", "폭발"]):
        return "#d63031"  # 빨강
    if any(k in text for k in ["좋아", "고마워", "다행"]):
        return "#00cec9"  # 민트
    return "#ffeaa7"  # 기본 노랑

st.title("🧠 Mumyeong GPT Prototype")
st.write("철학 기반 AI: 해석하지 않고, 기억하고, 존재하는...")

user_input = st.text_input("💬 Say something...", key="user_input")

if user_input:
    entry = collector.collect(user_input)
    st.session_state.log.append(entry)

    # 시각 반응 (침묵 기반)
    if entry["delay_since_last"] > 5:
        st.markdown("<div style='background-color:#dfe6e9; height:50px; border-radius:10px;'></div>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown("<div style='color:#636e72;'>🤫 침묵이 감지되었습니다.</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='font-size: 28px; color: {get_color_by_emotion(user_input)};'>● ● ●</div>", unsafe_allow_html=True)

    # 루프/회피 감지
    texts = [e["text"] for e in st.session_state.log]
    loop_detected = texts.count(user_input) > 1
    avoidance_keywords = ["괜찮", "그냥", "몰라", "비슷"]
    is_avoidance = any(word in user_input for word in avoidance_keywords)

    if loop_detected:
        st.warning("🔁 반복된 흐름이 감지되었습니다.")
    if is_avoidance:
        st.info("🌀 회피형 표현이 감지되었습니다.")

    # 프롬프트 생성
    prompt = generate_prompt(st.session_state.log)
    st.markdown("#### ✍️ 생성된 GPT 프롬프트")
    st.code(prompt, language="markdown")

    # AI 응답 (예시)
    st.markdown("#### 🤖 AI의 응답")
    st.success("이 구조... 익숙하지만, 미세하게 달라졌어요.")

# 📊 구조 흐름 시각화
if st.session_state.log:
    st.markdown("### 📊 구조 흐름 시각화")
    days = group_by_day(st.session_state.log)
    labels, counts = [], []
    for day, entries in days.items():
        labels.append(day)
        counts.append(len(entries))

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color="#81ecec")
    ax.set_ylabel("입력 수")
    ax.set_title("날짜별 사용자 감정 입력량")
    st.pyplot(fig)

# JSON 저장
if st.session_state.log:
    if st.button("📥 대화 기록 저장하기 (JSON)"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mumyeong_log_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(st.session_state.log, f, ensure_ascii=False, indent=2)
        with open(filename, "rb") as f:
            st.download_button("⬇️ 다운로드", data=f, file_name=filename, mime="application/json")
