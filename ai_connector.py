import requests

def call_huggingface_api(prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, dict) and "error" in result:
            return f"[API Error] {result['error']}"
        elif isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, list) and "generated_text" not in result[0]:
            return str(result[0])
        return str(result)
    else:
        return f"[Error {response.status_code}] {response.text}"
