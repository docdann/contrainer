import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controller import Controller


class DummyMsg:
    def __init__(self, payload: str):
        self.payload = payload.encode()


def test_on_message_updates_state():
    ctrl = Controller()
    payload = json.dumps({"node": "n1", "containers": []})
    ctrl.on_message(None, None, DummyMsg(payload))
    assert "n1" in ctrl.node_states
