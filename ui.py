import streamlit as st
import time
import json
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from input_collector import InputCollector
from prompt_generator import generate_prompt

st.set_page_config(page_title="🧠 Mumyeong GPT Prototype", layout="centered")

collector = InputCollector()
if "log" not in st.session_state:
    st.session_state.log = []

# Day 구조 생성
def group_by_day(log):
    result = defaultdict(list)
    for entry in log:
        dt = datetime.fromtimestamp(entry["timestamp"])
        day_key = dt.strftime("%Y-%m-%d")
        result[day_key].append(entry)
    return result

# 감정 색상
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

# 점 점점 사라짐 애니메이션
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

user_input = st.text_input("💬 Say something...", key="user_input")

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

    # 반복 & 회피 감지
    texts = [e["text"] for e in st.session_state.log]
    if texts.count(user_input) > 1:
        st.warning("🔁 반복된 흐름이 감지되었습니다.")
    if any(word in user_input for word in ["괜찮", "그냥", "몰라", "비슷"]):
        st.info("🌀 회피형 표현이 감지되었습니다.")

    # 프롬프트 + 응답
    prompt = generate_prompt(st.session_state.log)
    st.markdown("#### ✍️ GPT 프롬프트")
    st.code(prompt, language="markdown")

    # [무료 AI 연동 구조 위치]
    st.markdown("#### 🤖 AI 응답 (데모)")
    st.success("...이 말은 지난 흐름과 닮았지만, 이번엔 조금 달라요.")

# 📊 루프 타임라인 시각화
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

# 🧠 Day 30 구조 발화 예시
if len(set(group_by_day(st.session_state.log).keys())) >= 30:
    st.markdown("### 🧠 Day 30 구조 발화")
    st.info("너의 30일 흐름은 반복과 침묵이 주기적으로 나타나고 있어요. 그 안에 익숙함과 회피가 공존했어.")

# 📥 저장
if st.session_state.log:
    if st.button("📤 JSON 저장"):
        filename = f"mumyeong_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(st.session_state.log, f, ensure_ascii=False, indent=2)
        with open(filename, "rb") as f:
            st.download_button("⬇️ 다운로드", data=f, file_name=filename, mime="application/json")
