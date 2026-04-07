import os
from openai import OpenAI
from client import CareerEnv, CareerAction

# -------- ENV VARIABLES -------- #
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)

# -------- RUN ENVIRONMENT EPISODE -------- #
def run_episode():
    total_reward = 0.0

    # Initialize CareerEnv
    with CareerEnv(base_url="http://127.0.0.1:8000").sync() as env:

        # Reset environment
        result = env.reset()
        obs = result.observation

        # -------- START LOG -------- #
        print("[START]")
        print(f"scenario:{obs.scenario}")
        print(f"options:{obs.options}")

        done = False
        step = 0

        while not done and step < env.state.max_questions:
            step += 1

            # -------- BUILD PROMPT FOR LLM -------- #
            prompt = f"""
You are an AI career advisor.

Scenario:
{obs.scenario}

Options:
{obs.options}

Conversation so far:
{obs.conversation_history}

Ask a smart question OR give final recommendation.
Respond exactly in this format:
message:<text>
action_type:<ask/recommend>
"""

            # -------- LLM CALL -------- #
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            output = response.choices[0].message.content.strip()

            # -------- PARSE LLM OUTPUT -------- #
            try:
                lines = output.split("\n")
                message = lines[0].replace("message:", "").strip()
                action_type = lines[1].replace("action_type:", "").strip()
            except Exception:
                message = "What are your skills?"
                action_type = "ask"

            # -------- STEP ENV -------- #
            result = env.step(CareerAction(
                message=message,
                action_type=action_type
            ))

            obs = result.observation
            done = obs.done
            reward = obs.reward or 0.0
            total_reward += reward

            # -------- STEP LOG -------- #
            print("[STEP]")
            print(f"step:{step}")
            print(f"message:{message}")
            print(f"action_type:{action_type}")
            print(f"reward:{reward}")
            print(f"feedback:{obs.feedback}")

        # -------- END LOG -------- #
        print("[END]")
        print(f"total_reward:{total_reward}")

# -------- ENTRY POINT -------- #
if __name__ == "__main__":
    run_episode()