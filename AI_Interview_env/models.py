from typing import List, Optional, Dict
from openenv.core.env_server import Action, Observation, State


class CareerAction(Action):
    message: str
    action_type: str   # "ask" or "recommend"


class CareerObservation(Observation):
    user_profile: Dict[str, str]
    conversation_history: List[str]
    progress: float
    current_stage: str
    feedback: str


class CareerState(State):
    target_role: Optional[str] = None
    collected_answers: Dict[str, str] = {}
    questions_asked: int = 0
    max_questions: int = 5