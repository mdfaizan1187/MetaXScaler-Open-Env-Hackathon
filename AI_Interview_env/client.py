from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from .models import CareerAction, CareerObservation, CareerState


class CareerEnv(EnvClient[CareerAction, CareerObservation, CareerState]):

    def _step_payload(self, action: CareerAction) -> dict:
        return {
            "message": action.message,
            "action_type": action.action_type
        }

    def _parse_result(self, payload: dict) -> StepResult:
        obs = payload.get("observation", {})

        return StepResult(
            observation=CareerObservation(
                done=payload.get("done", False),
                reward=payload.get("reward"),
                scenario=obs.get("scenario", ""),
                options=obs.get("options", []),
                history=obs.get("history", []),
                score=obs.get("score", 0.0),
                message=obs.get("message", "")
            ),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: dict) -> CareerState:
        return CareerState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )