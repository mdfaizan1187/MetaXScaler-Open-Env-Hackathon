from openenv.core.env_server import create_fastapi_app
from .environment import CareerEnvironment
from models import CareerAction, CareerObservation

app = create_fastapi_app(
    CareerEnvironment,
    CareerAction,
    CareerObservation
)