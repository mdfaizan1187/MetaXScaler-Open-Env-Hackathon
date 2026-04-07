# MetaXScaler-Open-Env-Hackathon

# 🚀 AI Career Decision Environment (OpenEnv)

A real-world AI environment where an agent interviews a user, builds a profile, and recommends the best career decision using reinforcement-style interaction.

Built using **OpenEnv**, this project simulates real-life decision-making instead of toy problems.

---

## 📌 Overview

This environment allows an AI agent to:

* Ask intelligent questions
* Analyze user responses
* Build a structured profile
* Make a final career recommendation

The system provides **step-by-step rewards**, encouraging better questioning and decision-making.

---

## 🧠 Key Features

* ✅ Real-world simulation (career decision-making)
* ✅ Multi-step interaction (interview style)
* ✅ Reward shaping (partial + final rewards)
* ✅ 3 difficulty levels (easy, medium, hard)
* ✅ OpenEnv compatible (`reset()`, `step()`, `state()`)
* ✅ Fully deployable (FastAPI + Docker + Hugging Face)

---

## 🏗️ Project Structure

```
AI_Interview_env/
│
├── server/
│   ├── __init__.py
│   ├── app.py              # FastAPI server
│   ├── environment.py      # Core environment logic
│
├── models.py               # Action, Observation, State models
├── inference.py            # Baseline agent (mandatory)
├── openenv.yaml            # OpenEnv specification
├── requirements.txt        # Dependencies
├── Dockerfile              # Deployment container
├── README.md               # Documentation
```

---

## ⚙️ Environment Design

### 🔹 Action Space

```json
{
  "message": "string",
  "action_type": "ask | recommend"
}
```

### 🔹 Observation Space

* scenario: problem description
* options: possible decisions
* user_profile: collected answers
* conversation_history: full interaction
* progress: completion percentage
* current_stage: easy / medium / hard / final
* feedback: quality of agent decision

---

## 🎯 Tasks

| Task        | Difficulty | Description                   |
| ----------- | ---------- | ----------------------------- |
| easy_task   | Easy       | Beginner career choice        |
| medium_task | Medium     | Career switch decision        |
| hard_task   | Hard       | Complex multi-option scenario |

---

## 🏆 Reward System

* **Partial Reward:** Based on quality of questions (keyword matching)
* **Final Reward:** Based on profile completeness and decision
* Range: `0.0 → 1.0`

---

## ▶️ How to Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start server

```bash
uvicorn server.app:app --reload
```

### 3️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

### 4️⃣ Run inference agent

```bash
python inference.py
```

---

## 🤖 Inference Requirements

Set environment variables:

```bash
API_BASE_URL=http://127.0.0.1:8000
MODEL_NAME=<your-model>
HF_TOKEN=<your-token>
```

Logs follow strict format:

```
[START]
[STEP]
[END]
```

---

## 🐳 Docker Support

### Build:

```bash
docker build -t ai-career-env .
```

### Run:

```bash
docker run -p 8000:8000 ai-career-env
```

---

## 🌐 Hugging Face Deployment

* Create a Space (Gradio / Python)
* Upload all files
* Ensure `server.app:app` runs correctly
* Test `/reset` and `/step` endpoints

---

## 🧪 Validation Checklist

* ✅ API responds (`/reset`, `/step`)
* ✅ `openenv.yaml` valid
* ✅ 3 tasks implemented
* ✅ Rewards in range (0.0–1.0)
* ✅ `inference.py` runs successfully
* ✅ Docker builds correctly

---

## 🚀 Future Improvements

* Real user interaction (replace simulated responses)
* Smarter reward functions
* Personalized career paths
* Multi-agent negotiation system

---

## 👨‍💻 Author

**Faizan**
AI Hackathon Project 🚀

---

## ⭐ Key Insight

This project demonstrates how **AI agents can learn real-world decision-making** using environment-based training instead of static datasets.

---

🔥 Built for OpenEnv Hackathon — Real Problems, Real Intelligence.
