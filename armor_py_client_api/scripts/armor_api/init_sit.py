#! /usr/bin/env python

from armor_client import ArmorClient
from os.path import dirname, realpath

"""
this client starts the sit
then get the name of the ontology
It calls init command defined in ArmorCommandExecutive
"""

client = ArmorClient("client", "reference")
client.call("INIT","","",[])
client.utils.set_log_to_terminal(True)


