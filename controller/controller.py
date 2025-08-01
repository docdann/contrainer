import json
import paho.mqtt.client as mqtt


class Controller:
    def __init__(self, mqtt_host: str = "localhost", mqtt_port: int = 1883):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.node_states: dict[str, dict] = {}

    def connect(self) -> None:
        """Connect to the MQTT broker and subscribe to heartbeat messages."""
        self.client.connect(self.mqtt_host, self.mqtt_port)
        self.client.subscribe("heartbeat/#")
        self.client.loop_start()

    def on_message(self, client, userdata, msg) -> None:
        payload = msg.payload.decode()
        try:
            state = json.loads(payload)
        except json.JSONDecodeError:
            return
        node_id = state.get("node")
        if not node_id:
            return
        self.node_states[node_id] = state

    def send_command(self, node_id: str, command: dict) -> None:
        """Publish a command for a specific node."""
        payload = json.dumps(command)
        self.client.publish(f"command/{node_id}", payload)
