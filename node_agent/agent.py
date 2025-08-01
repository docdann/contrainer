import json
import paho.mqtt.client as mqtt


class NodeAgent:
    def __init__(self, node_id: str, mqtt_host: str = "localhost", mqtt_port: int = 1883):
        self.node_id = node_id
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.last_command = None

    def connect(self) -> None:
        """Connect to the MQTT broker and begin listening for commands."""
        self.client.connect(self.mqtt_host, self.mqtt_port)
        self.client.subscribe(f"command/{self.node_id}")
        self.client.loop_start()

    def send_heartbeat(self, containers=None) -> None:
        """Publish a heartbeat message with container info."""
        if containers is None:
            containers = []
        payload = json.dumps({"node": self.node_id, "containers": containers})
        self.client.publish(f"heartbeat/{self.node_id}", payload)

    def on_message(self, client, userdata, msg) -> None:
        payload = msg.payload.decode()
        try:
            command = json.loads(payload)
        except json.JSONDecodeError:
            return
        self.handle_command(command)

    def handle_command(self, command: dict) -> None:
        """Handle a command received from the controller."""
        self.last_command = command
        # In a real agent, Docker/Podman operations would occur here.
        print(f"Received command for {self.node_id}: {command}")


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Run a node agent")
    parser.add_argument(
        "node_id",
        nargs="?",
        default=os.environ.get("NODE_ID"),
        help="Unique identifier for this node",
    )
    parser.add_argument(
        "--mqtt-host",
        default=os.environ.get("MQTT_HOST", "localhost"),
        help="Hostname of the MQTT broker",
    )
    parser.add_argument(
        "--mqtt-port",
        type=int,
        default=int(os.environ.get("MQTT_PORT", 1883)),
        help="Port of the MQTT broker",
    )
    args = parser.parse_args()

    if not args.node_id:
        parser.error("node_id is required (set NODE_ID env var or pass as arg)")

    agent = NodeAgent(
        args.node_id, mqtt_host=args.mqtt_host, mqtt_port=args.mqtt_port
    )
    agent.connect()
    agent.send_heartbeat()
    print(f"Node agent {args.node_id} running. Press Ctrl-C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
