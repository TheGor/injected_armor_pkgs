# ArmorPy
A python client library for **ARMOR** originally hosted by [EMAROlab](https://github.com/EmaroLab/armor_py_api).

Allows users to easily call ARMOR service from Python code.

**Full documentation** at:

http://emarolab.github.io/armor_py_api/

Hides ROS service calls to ARMOR in utility functions whose structure is 
similar to that of OWL API. ARMOR is a powerful tool able to manage, query
and modify multiple ontologies in a safe way. It also include several macros
to perform complex manipulations on ARMOR references (manipulations that
usually require more than a few line of codes in OWL APIs, such as replacing
a specific data property value associated to an individual).

More functions are coming soon as their needed.

ArmorPy installs itself into the */devel/bin* of your workspace as you run
*catkin_make install*. It is then available to all your ROS Python packages.

To use it, import from 'armor_api':

    from armor_api.armor_client import ArmorClient

If your IDE cannot find the ArmorPy sources when working on a different 
project, you have to add armor_py_api/scripts/armor_api as a source folder.

In PyCharm you can add a folder as a source in the menu:

**Settings...-> Project: your_project_name-> Project Structure**.

**Note:** if your workspace is corrrectly set, installing ArmorPy is enough to
use it in your code and run it. Thus, even if your IDE cannot find your imports,
your code will work (it should find an **\_\_init\_\_.py** file only). Adding sources
will allow you to see ArmorPy code for quick reference, easier debugging and 
getting rid of annoying warnings.

# New python clients

[load_ontology_amor](https://github.com/TheGor/injected_armor_pkgs/blob/developingMine/armor_py_client_api/scripts/armor_api/load_ontology_amor.py) sends the ontology file to AMOR by given the predefined command “LOAD” and the path to the ontology file as parameter of the service request.

[init_sit](https://github.com/TheGor/injected_armor_pkgs/blob/developingMine/armor_py_client_api/scripts/armor_api/init_sit.py) that is responsible for activating SIT by passing the ontology file, previously loaded in AMOR.

[publisher_send_scene](https://github.com/TheGor/injected_armor_pkgs/blob/developingMine/armor_py_client_api/scripts/armor_api/publisher_send_scene.py) simulates the functionality of PIT by defining some fixed table-top scenario with two or three objects thanks to messages and ArmorObjects.

[clean_ontology](https://github.com/TheGor/injected_armor_pkgs/blob/developingMine/armor_py_client_api/scripts/armor_api/clean_ontology.py) is responsible for eliminating all individuals contained in the ontology

[state_machine](https://github.com/TheGor/injected_armor_pkgs/blob/developingMine/armor_py_client_api/scripts/armor_api/state_machine.py) shows a complete simulation of the robot behaviour (see report ) 

# Author
 - [alessio.capitanelli@dibris.unige.it](mailto:alessio.capitanelli@dibris.unige.it).
