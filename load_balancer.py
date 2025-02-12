"""

Design a Load Balancer API to distribute requests to multiple backend servers.

Register a Server - Add a new backend server to the load balancer.
Deregister a Server - Remove a backend server from the load balancer.
Route a Request - Forward an incoming request to one of the available servers.
Handle Server Failures - Detect and remove unresponsive servers.
Support Load Balancing Strategy - Distribute requests based on Round Robin (default).
Retrieve Active Servers - Get a list of currently available servers.

"""
from typing import List, Optional

class Server:
    def __init__(self, server_id: str):
        self.server_id = server_id
        self.is_alive = True  # Assume all servers are initially alive

    def handle_request(self, request: str):
        if self.is_alive:
            print(f"Server {self.server_id} handling request: {request}")
        else:
            raise Exception(f"Server {self.server_id} is down!")

    def mark_down(self):
        self.is_alive = False

    def mark_up(self):
        self.is_alive = True

class LoadBalancer:
    def __init__(self):
        self.servers: List[Server] = []
        self.current_index = 0  # To implement Round Robin strategy

    def add_server(self, server: Server):
        self.servers.append(server)

    def remove_server(self, server_id: str):
        self.servers = [server for server in self.servers if server.server_id != server_id]

    def get_next_server(self) -> Optional[Server]:
        if not self.servers:
            return None  # No servers available
        for _ in range(len(self.servers)):  # To avoid infinite loops if all servers are down
            server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)
            if server.is_alive:
                return server
        return None  # All servers are down

    def route_request(self, request: str):
        server = self.get_next_server()
        if server:
            server.handle_request(request)
        else:
            print("No available servers to handle the request.")

# Example Usage
lb = LoadBalancer()
server1 = Server("S1")
server2 = Server("S2")
server3 = Server("S3")

lb.add_server(server1)
lb.add_server(server2)
lb.add_server(server3)

# Simulating request routing
lb.route_request("Request 1")
lb.route_request("Request 2")

# Simulating a server failure
server2.mark_down()
lb.route_request("Request 3")

# Removing a server
lb.remove_server("S1")
lb.route_request("Request 4")