#! /usr/bin/env python

from armor_client import ArmorClient
from os.path import dirname, realpath

__author__ = "Alessio Capitanelli"
__copyright__ = "Copyright 2016, ArmorPy"
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Alessio Capitanelli"
__email__ = "alessio.capitanelli@dibris.unige.it"
__status__ = "Development"

# INITIALIZE REFERENCE
#this client starts the sit
#then get the name of the ontology

client = ArmorClient("client", "reference")
client.call("CLEAN","","",["Sphere","Plane"])
client.utils.set_log_to_terminal(True)
