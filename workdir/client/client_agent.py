import base64
import hashlib
import binascii
from typing import List

import oef
from oef.agents import OEFAgent
from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


import agent_dataModel
from agent_dataModel import TIME_AGENT

import json
import datetime

import sys
import time
import uuid
import asyncio

class ClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """
    def __init__(self, public_key: str, oef_addr: str, oef_port: int = 10000):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        print("Received message: origin={}, dialogue_id={}, content={}".format(origin, dialogue_id, content))
        data = json.loads(content.decode())
        print ("message...")
        print(data)

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))

        for agent in agents:

            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            self.pending_cfp += 1
            self.send_cfp(1, 0, agent, 0, None)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))
        #print(dialogue_id)

        for i,p in enumerate(proposals):
            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})

        received_cfp = len(self.received_proposals) + self.received_declines

        # once everyone has responded, let's accept them.
        if received_cfp == self.pending_cfp :
            print("I am here")
            if len( self.received_proposals) >= 1 :
                self.send_accept(msg_id,dialogue_id,self.received_proposals[0]['agent'],msg_id + 1)
                print ("Accept")
            else :
                print("They don't have data")
                self.stop()

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("Received a decline!")
        self.received_declines += 1

if __name__ == '__main__':

    # define an OEF Agent
    client_agent = ClientAgent(str(uuid.uuid4()), oef_addr="127.0.0.1", oef_port=10000)

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query1 = Query([Constraint("timezone", Eq(3)), Constraint("twentyfour", Eq(False))],TIME_AGENT())


    client_agent.search_services(0, echo_query1)
    client_agent.run()
