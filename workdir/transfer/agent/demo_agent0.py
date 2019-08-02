import oef
from oef.agents import OEFAgent

import os, sys
import json
import time


from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

import agent_dataModel
from agent_dataModel import TIME_AGENT

import random
import json
import datetime
import copy

import asyncio

import uuid
import time

class Demo_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 3333):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())

        self.scheme = {}
        self.scheme['timezone'] = None
        self.scheme['id'] = None

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        #data = self.get_latest(0)
        proposal = Description({"data" : True})
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        command = {}
        command["time"] = int(time.time())
        msg = json.dumps(command)
        self.send_message(0,dialogue_id, origin, msg.encode())


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


if __name__ == '__main__':

    # create agent and connect it to OEF
    server_agent = Demo_Agent("Time{}".format(str(random.randint(0,9999999999999))), oef_addr="127.0.0.1", oef_port=3333)
    server_agent.scheme['timezone'] = 3
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.scheme['twentyfour'] = True
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, TIME_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()
