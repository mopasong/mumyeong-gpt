import time
import json

class InputCollector:
    def __init__(self):
        self.last_input_time = time.time()
        self.log = []

    def collect(self, user_input):
        now = time.time()
        delay = now - self.last_input_time
        self.last_input_time = now

        entry = {
            "timestamp": now,
            "text": user_input,
            "delay_since_last": delay,
            "type": "text" if user_input else "silence"
        }

        self.log.append(entry)
        return entry

    def save_log(self, filename="input_log.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)