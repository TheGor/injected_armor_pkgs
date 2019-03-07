#! /usr/bin/env python

"""
A simple test script that loads an ontology
It uses command Load defined in ArmorCommandExecutive 
"""

from armor_client import ArmorClient
from os.path import dirname, realpath

# this client load the ontology empty scene


path = dirname(realpath(__file__))
path = path + "/../../test/"

client = ArmorClient("client", "reference")
client.utils.load_ref_from_file(path + "empty-scene.owl", "http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit",
                                True, "PELLET", True, False)  
client.utils.mount_on_ref()
client.utils.set_log_to_terminal(True)





