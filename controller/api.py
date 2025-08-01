from fastapi import FastAPI

import os

from .controller import Controller

controller = Controller(
    mqtt_host=os.environ.get("MQTT_HOST", "localhost"),
    mqtt_port=int(os.environ.get("MQTT_PORT", 1883)),
)
app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    controller.connect()


@app.get("/nodes")
async def get_nodes() -> dict[str, dict]:
    return controller.node_states
