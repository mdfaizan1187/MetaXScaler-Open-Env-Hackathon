from openenv.core.env_server import Environment
from models import CareerAction, CareerObservation, CareerState
import uuid
import random

# ------------------ SCENARIOS ------------------ #
SCENARIOS = [
    {
        "id": "easy_1",
        "difficulty": "easy",
        "description": "You are a student with basic coding skills. You got an offer for a low-paying job and also an option to learn advanced AI for 6 months.",
        "options": [
            "Take the job",
            "Study AI for 6 months",
            "Do both part-time"
        ],
        "correct": 1
    },
    {
        "id": "medium_1",
        "difficulty": "medium",
        "description": "You have 2 years experience. You can switch to a startup (high risk, high growth) or stay in a stable job.",
        "options": [
            "Stay in current job",
            "Join startup",
            "Prepare for higher studies"
        ],
        "correct": 1
    },
    {
        "id": "hard_1",
        "difficulty": "hard",
        "description": "You have multiple offers: high salary abroad, startup founder opportunity, or government job.",
        "options": [
            "Go abroad",
            "Start your own company",
            "Take government job"
        ],
        "correct": 1
    }
]


# ------------------ ENVIRONMENT ------------------ #
class CareerEnvironment(Environment):

    def __init__(self):
        self._state = CareerState()
        self._history = []
        self._profile = {}
        self.current = None

    # -------- RESET -------- #
    def reset(self, **kwargs) -> CareerObservation:
        self.current = random.choice(SCENARIOS)

        self._state = CareerState(
            episode_id=str(uuid.uuid4()),
            step_count=0
        )

        self._state.max_questions = 5
        self._history = []
        self._profile = {}

        return CareerObservation(
            done=False,
            reward=None,
            scenario=self.current["description"],
            options=self.current["options"],
            history=[],
            score=0.0,
            message="Start interview by asking relevant questions."
        )

    # -------- STEP -------- #
    def step(self, action: CareerAction, **kwargs) -> CareerObservation:
        self._state.step_count += 1

        message = action.message.lower().strip()
        action_type = action.action_type

        # Store AI question
        self._history.append(f"AI: {message}")

        # Simulate user response
        user_response = self._simulate_user_response(message)
        self._history.append(f"User: {user_response}")

        # Store profile
        key = f"q{self._state.step_count}"
        self._profile[key] = user_response

        # -------- PARTIAL REWARD -------- #
        keywords = self._expected_keywords()
        match_count = sum(1 for k in keywords if k in message)
        step_reward = match_count / len(keywords) if keywords else 0.0

        # -------- PROGRESS -------- #
        progress = min(1.0, self._state.step_count / self._state.max_questions)

        # -------- FEEDBACK -------- #
        if step_reward > 0.6:
            feedback = "Good question 👍"
        elif step_reward > 0.3:
            feedback = "Average question ⚠️"
        else:
            feedback = "Weak question ❌"

        done = False
        final_reward = step_reward

        # -------- FINAL DECISION -------- #
        if action_type == "recommend" or progress >= 1.0:
            done = True

            decision_index = self._extract_decision(message)
            correct_index = self.current["correct"]

            if decision_index == correct_index:
                decision_reward = 1.0
                decision_feedback = "Correct career decision 🎯"
            else:
                decision_reward = 0.0
                decision_feedback = "Suboptimal decision ❌"

            final_reward = (step_reward + decision_reward) / 2
            feedback = decision_feedback

        return CareerObservation(
            done=done,
            reward=final_reward,
            scenario=self.current["description"],
            options=self.current["options"],
            history=self._history,
            score=final_reward,
            message=feedback
        )

    # -------- STATE -------- #
    @property
    def state(self) -> CareerState:
        return self._state

    # -------- HELPERS -------- #

    def _simulate_user_response(self, question: str) -> str:
        responses = [
            "I have some experience in coding and projects.",
            "I enjoy solving problems and learning new technologies.",
            "I am interested in startups and innovation.",
            "I prefer stability but also want growth.",
            "I like working with data and AI systems."
        ]
        return responses[self._state.step_count % len(responses)]

    def _calculate_reward(self) -> float:
        return 1.0 if len(self._profile) >= 3 else 0.5

    def _expected_keywords(self):
        return ["experience", "skills", "growth", "risk", "learning"]

    def _extract_decision(self, message: str) -> int:
        for i, option in enumerate(self.current["options"]):
            if option.lower() in message:
                return i
        return -1