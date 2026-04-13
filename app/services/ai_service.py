import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_user_input(user_text: str):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Convert user input into STRICT JSON with keys: action and task."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)

        # FALLBACK (mock logic)
        text = user_text.lower()

        actions = []

        # MISSED
        if "miss" in text:
            actions.append({"action": "mark_missed", "task": "gym"})

        # DONE / COMPLETED
        if "done" in text or "complete" in text or "completed" in text:
            actions.append({"action": "mark_done", "task": "gym"})

        # STUDY
        if "study" in text or "learn" in text:
            actions.append({"action": "mark_done", "task": "study"})

        # fallback default
        if not actions:
            actions.append({"action": "mark_done", "task": "task"})

        return json.dumps(actions)
    