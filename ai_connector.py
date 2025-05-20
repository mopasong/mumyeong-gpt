import requests

def call_huggingface_api(prompt, token):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
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
        if isinstance(result, list):
            return result[0].get("generated_text", str(result[0]))
        return str(result)
    else:
        return f"[Error {response.status_code}] {response.text}"
