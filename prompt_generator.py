def generate_prompt(history):
    last_entry = history[-1] if history else {}
    text = last_entry.get("text", "")
    delay = last_entry.get("delay_since_last", 0)

    prompt = "[Context]\n"
    prompt += "- 이 시스템은 사용자의 반복, 침묵, 회피 패턴을 감지합니다.\n"
    prompt += "- 감정을 해석하거나 이름 붙이지 않고, 구조만 반영합니다.\n\n"
    prompt += "[Instruction]\n"
    prompt += "- 감정 명명 금지\n"
    prompt += "- 침묵은 '존재'로 반응\n"
    prompt += "- 반복 감지 시 리듬 기반 응답\n\n"
    prompt += "[User Input]\n"
    prompt += f"{text}\n\n"
    prompt += "[System Note]\n"
    prompt += f"- 입력 간 간격: {delay:.2f}초\n"

    return prompt