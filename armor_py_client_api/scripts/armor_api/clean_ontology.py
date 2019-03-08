#! /usr/bin/env python

from armor_client import ArmorClient
from os.path import dirname, realpath


"""
this client cleans the ontology by removing all individuals
"""

client = ArmorClient("client", "reference")
client.call("CLEAN","","",["GeometricPrimitive"])
client.utils.set_log_to_terminal(True)
