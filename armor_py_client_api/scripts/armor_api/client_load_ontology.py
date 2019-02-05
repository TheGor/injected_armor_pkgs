#! /usr/bin/env python

"""
A client that call armor to load an ontology file
"""

from armor_client import ArmorClient

# INITIALIZE REFERENCE

#path = dirname(realpath(__file__))
#path = path + "/../../test/"

client = ArmorClient("client", "reference")
client.call("INITSIT","","",[]);
client.utils.set_log_to_terminal(True)

