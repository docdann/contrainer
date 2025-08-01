Here’s a high-level outline of your MQTT-powered distributed container lifecycle management system:
🧩 Project Overview

This project enables a central controller container to orchestrate and manage remote containers running on multiple node machines, using MQTT as a lightweight, scalable pub/sub communication protocol.
🏗️ System Components
1. MQTT Broker

    Acts as the messaging hub for communication.

    Handles all pub/sub topics for heartbeats and control commands.

    Examples: Mosquitto, EMQX, HiveMQ.

2. Controller Service (API + MQTT Sub)

    Receives status/heartbeat updates from remote nodes via MQTT (heartbeat/<node_id>).

    Sends commands like container start/stop via MQTT (command/<node_id>).

    Exposes a REST API for clients (dashboard, CLI, etc.) to:

        View node/container status

        Dispatch commands to nodes

        Monitor system health

3. Node Agent (runs on each machine)

    Connects to MQTT broker.

    Publishes:

        heartbeat/<node_id> with current containers and system info.

    Subscribes to:

        command/<node_id> for actions like start, stop, or remove.

    Uses Docker or Podman to execute lifecycle actions locally.

📡 Communication Model

All communication flows through MQTT topics:
Topic Pattern	Publisher	Subscriber	Purpose
heartbeat/<node_id>	Node Agent	Controller	Node reports its status
command/<node_id>	Controller	Node Agent	Commands for container control

Optional enhancements:

    status/<node_id> (if agents want to send back execution results)

    logs/<node_id>/<container_id> (for log streaming)

🎯 Key Features

    ✅ Node discovery & registration via heartbeat

    ✅ Remote container start/stop/restart

    ✅ Centralized state monitoring

    ✅ API access to system status and control

    ✅ Lightweight and scalable communication with MQTT

    ✅ Platform-agnostic (Docker or Podman)

🧰 Technologies Used
Role	Tech
Messaging	MQTT (Mosquitto)
Controller API	FastAPI or Flask (Python)
Container Mgmt	Docker SDK / Podman API
Node Agent	Python (paho-mqtt + docker)
Deployment	Docker Compose / systemd
Optional DB	Redis or PostgreSQL
🧪 Example Use Cases

    ✅ Run containerized jobs on edge/IoT devices from a centralized controller

    ✅ Automatically deploy and manage services across a fleet of machines

    ✅ Monitor containerized applications in a custom DevOps setup

    ✅ Build a lightweight alternative to Kubernetes or Docker Swarm


## Development

Run the test suite in a container using Docker Compose:

```bash
docker compose run --rm tests
```

## Usage

### Running the Controller (master)

Launch the API service locally with uvicorn:

```bash
uvicorn controller.api:app --reload
```

The controller uses `MQTT_HOST` and `MQTT_PORT` to locate the broker.

### Running a Node Agent (client)

```bash
python -m node_agent.agent NODE_ID
```

Use the same `MQTT_HOST` and `MQTT_PORT` variables so the agent can connect to the broker used by the controller.

### Docker Compose

All components can be started together in containers:

```bash
docker compose up --build
```

The controller will be reachable at `http://localhost:8000` and the broker at `localhost:1883`.

### Continuous Integration

A GitHub Actions workflow in `.github/workflows/ci.yml` installs dependencies and runs `pytest` automatically on pushes and pull requests.
