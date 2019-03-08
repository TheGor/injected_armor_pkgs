# injected_armor
an extention of [ARMOR](https://arxiv.org/abs/1706.10151) with OWLOOP and the injected service SIT.

# Overview 

This repository contains a [ROSJAVA](http://wiki.ros.org/rosjava) packages for managing OWL ontologies in a robotic architecture.
The repository contains three ROS packages:
- [injected_armor_msgs](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/injected_armor_msgs): contains the definition of the messages for interacting with the ontology through ARMOR ROS service.
- [injected_armor](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/injected_armor): contains the services and libraries for interacting with OWL ontologies.
- [armor_py_client_api](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/armor_py_client_api): contains an example, a test script,common utility fot using ARMOR from a Python ROS client and a Ros Smach State Machine. 

The `injected_armor` package contains three modules:
- [amor](https://github.com/EmaroLab/injected_armor_pkgs/tree/master/injected_armor/amor): is the Java library that interacts with OWL API and Reasoners in a trade safe manner. This is the core for using OWL ontologies.
- [owloop](https://github.com/EmaroLab/injected_armor_pkgs/tree/master/injected_armor/owloop): is an extension of `amor` that allows to interact with ontology in an Object Oriented Programming manner.
- [armor](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/injected_armor/armor): is a ROS service that depends on `amor` and `injected_armor_msgs` for allow ROS clients to manipulate ontologies from other packages.
- [sit](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/injected_armor/sit): is a library that implements the Scene Identification and Tagging (SIT) algorithm. It depends on `owloop` (which consequentially depends on `amor`). This library should be used by `armor` in order to inject a new service. 
- [client_api_java](https://github.com/TheGor/injected_armor_pkgs/tree/developingMine/injected_armor/client_api_java): is a client that simulates the sending of scenes

Please check the `README` file and `Doc` folder inside each components of the above lists for more information. 
All of them have been imported from their original repository, which is linked inside the documentation of each module.

# Instalation

This repository must be a child of the src folder in your workspace to reach the maven repository (set in the `build.gradle` inside each module as `../../../../devel/share/maven/`).

# Prerequisites 

 - Install Ros Kinetic (see http://wiki.ros.org/)
 - Install Rosjava (see: http://wiki.ros.org/rosjava)
 - Install Smach (see: http://wiki.ros.org/smach)
 - Install RosPy (see: http://wiki.ros.org/rospy)

# How to run

In order to perform the state machine, the following steps are required:
(It suggested to run every of these commands in different terminal) 

1.	Roscore
2.	Rosrun armor_py_client_api state_machine.py
3.	Rosrun armor_py_client_api publisher_send_scene.py
4.	Rosrun injected_armor armor it.emarolab.armor.ARMORMainService

In order to launch every single client, the following steps are required:
(It suggested to run every of these commands in different terminal)

1.	Roscore
2.	Rosrun injected_armor armor it.emarolab.armor.ARMORMainService
3.	Rosrun armor_py_client_api load_ontology_armor.py
4.	Rosrun armor_py_client_api init_sit.py
5.	Rosrun injected_armor client_api_java com.rosjava.github.injected_armor.client_api_java.ClientSendObject
6.	Rosrun armor_py_client_api clean_ontology.py


## Contacts

For comment, discussions or support refer to this git repository open issues before to contact us (more detailed contacts to the authors is further specified in each module)
 - [luca.buoncompagni@edu.unige.it](mailto:luca.buoncompagni@edu.unige.it).


