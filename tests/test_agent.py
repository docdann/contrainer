import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from node_agent import NodeAgent


def test_handle_command():
    agent = NodeAgent("test")
    cmd = {"action": "start", "container": "alpine"}
    agent.handle_command(cmd)
    assert agent.last_command == cmd
