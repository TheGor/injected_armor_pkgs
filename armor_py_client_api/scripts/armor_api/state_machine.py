#!/usr/bin/env python

import rospy
import smach
import smach_ros
import injected_armor_msgs.srv
from injected_armor_msgs.srv import ArmorDirective,ArmorDirectiveRequest,ArmorObjects,ArmorObjectsRequest
import injected_armor_msgs.msg
from injected_armor_msgs.msg import SphereMSG,PlaneMSG,ListObjects
from os.path import dirname, realpath
import random
from std_msgs.msg import Int16
import time

path = dirname(realpath(__file__))
path = path + "/../../test/empty-scene.owl"



class Look(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2','outcome3','failed'])
	#if we received 1 we get scene1, if 2 we get scene2 and if 3 we get scene3	
	self.one_received = False
	self.two_received = False
	self.three_received = False
	#call the subscriber
	#This declares that your node subscribes to the chatter topic which is of type Int64. When new messages are received, 		      		#callback is invoked with the message as the first argument.
        self.subscriber = rospy.Subscriber('chatter', Int16, self.callback)

    def callback(self, data):
  	if data.data == 1:
            self.one_received = True
        elif data.data == 2:
            self.two_received = True
        elif data.data == 3:
            self.three_received = True
       

    def execute(self,userdata):
	rospy.loginfo('Executing state Scene')
	#rospy.loginfo('flag = %f'%data.data)
	time.sleep(10)
	if self.one_received:
		return 'outcome1'
	elif self.two_received:
		return 'outcome2'
	elif self.three_received:
		return 'outcome3'
	else:
		return 'failed'

	

def main():
	rospy.init_node('state_machine_robot')

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['succeeded','preempted','aborted'])	
	
	with sm:
		#define function for loading an ontology, with armorDirectiveSrv
		def set_ontology_request_cb(userdata,request):
			set_ontology_request = ArmorDirectiveRequest()
			set_ontology_request.armor_request.client_name = "client"
			set_ontology_request.armor_request.reference_name = "reference"
			set_ontology_request.armor_request.command = "LOAD"
			set_ontology_request.armor_request.primary_command_spec = "FILE"
			set_ontology_request.armor_request.secondary_command_spec = ""
			set_ontology_request.armor_request.args = [path,"http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit",str(True),"PELLET",str(False)]

			return set_ontology_request
			
		#creating the load ontology state
		smach.StateMachine.add('LOAD_ONTOLOGY',smach_ros.ServiceState('armor_interface_srv',ArmorDirective,request_cb = 									set_ontology_request_cb),transitions={'succeeded':'INIT_SIT'})

		#define funciton for init sit, it uses the armordirectivesrv

		def get_ontology_request_cb(userdata,request):
			get_ontology_request = ArmorDirectiveRequest()
			get_ontology_request.armor_request.client_name = "client"
			get_ontology_request.armor_request.reference_name = "reference"
			get_ontology_request.armor_request.command = "INIT"
			
			return get_ontology_request

		#create the state for init sit

		smach.StateMachine.add('INIT_SIT',smach_ros.ServiceState('armor_interface_srv',ArmorDirective,request_cb = 											get_ontology_request_cb),transitions={'succeeded':'LOOK'})


		#create state scene as a switch
		smach.StateMachine.add('LOOK',Look(),transitions={'outcome1':'LOOK_SCENE1',
								    'outcome2':'LOOK_SCENE2',
								     'outcome3':'LOOK_SCENE3',
									'failed': 'aborted'}) 


		#define function for passing object data
		def sceneone_request_cb(userdata,request):
			objects1= ListObjects()
			objects2= ListObjects()
			object1 = SphereMSG()
			object2 = PlaneMSG()
			sceneone_request = ArmorObjectsRequest()
			#Definition Sphere
			object1.radiusmsg = 0.1
			object1.centermsg.xmsg = 0.3
			object1.centermsg.ymsg = 0.3
			object1.centermsg.zmsg = 0.3
			#Definition Plane
			object2.hessianmsg = 0.6
			object2.centermsg.xmsg = 0.6
			object2.centermsg.ymsg = 0.6
			object2.centermsg.zmsg = 0.6
			object2.axismsg.ax = 0.5
			object2.axismsg.ay = 0.5
			object2.axismsg.az = 0.5
			objects1.sfera = object1
			objects2.piano = object2
				
			#Definition Request
			sceneone_request.thing = [objects1,objects2]
			sceneone_request.name_object = ["Sphere","Plane"]
			
			return sceneone_request
		
		#define scene1 (plane,sphere) state
		smach.StateMachine.add('LOOK_SCENE1',smach_ros.ServiceState('send_objects',ArmorObjects,request_cb = 									sceneone_request_cb))


	#definition scene 2
	#define function for passing object data
		def scenetwo_request_cb(userdata,request):
			objects1= ListObjects()
			objects2= ListObjects()
			object1 = SphereMSG()
			object2 = SphereMSG()
			scenetwo_request = ArmorObjectsRequest()
			#Definition Sphere
			object1.radiusmsg = 0.1
			object1.centermsg.xmsg = 0.3
			object1.centermsg.ymsg = 0.3
			object1.centermsg.zmsg = 0.3
			#Definition Plane
			object2.radiusmsg = 5.0
			object2.centermsg.xmsg = 3.0
			object2.centermsg.ymsg = 3.0
			object2.centermsg.zmsg = 3.0

			objects1.sfera = object1
			objects2.sfera = object2
				
			#Definition Request
			scenetwo_request.thing = [objects1,objects2]
			scenetwo_request.name_object = ["Sphere","Sphere"]
			
			return scenetwo_request
		
		#define scene2 state (sphere,sphere)
		smach.StateMachine.add('LOOK_SCENE2',smach_ros.ServiceState('send_objects',ArmorObjects,request_cb = 									scenetwo_request_cb))


	#definition scene 2
	#define function for passing object data
		def scenethree_request_cb(userdata,request):
			objects1= ListObjects()
			objects2= ListObjects()
			objects3= ListObjects()
			object1 = SphereMSG()
			object2 = SphereMSG()
			object3 = PlaneMSG()
			scenethree_request = ArmorObjectsRequest()
			#Definition Sphere
			object1.radiusmsg = 0.1
			object1.centermsg.xmsg = 0.3
			object1.centermsg.ymsg = 0.3
			object1.centermsg.zmsg = 0.3
			#Definition Plane
			object2.radiusmsg = 5.0
			object2.centermsg.xmsg = 3.0
			object2.centermsg.ymsg = 3.0
			object2.centermsg.zmsg = 3.0
			#Definition Plane
			object3.hessianmsg = 0.6
			object3.centermsg.xmsg = 0.6
			object3.centermsg.ymsg = 0.6
			object3.centermsg.zmsg = 0.6
			object3.axismsg.ax = 0.5
			object3.axismsg.ay = 0.5
			object3.axismsg.az = 0.5

			objects1.sfera = object1
			objects2.sfera = object2
			objects3.piano = object3
				
			#Definition Request
			scenethree_request.thing = [objects1,objects2,objects3]
			scenethree_request.name_object = ["Sphere","Sphere","Plane"]
			
			return scenethree_request
		
		#define scene3 state (plane,sphere,sphere)
		smach.StateMachine.add('LOOK_SCENE3',smach_ros.ServiceState('send_objects',ArmorObjects,request_cb = 									scenethree_request_cb))



	#result = sm.execute()
    	#rospy.loginfo(result)    
	# Attach a SMACH introspection server
    	sis = smach_ros.IntrospectionServer('smach_usecase_01', sm, '/USE_CASE')
    	sis.start()

    	# Execute SMACH tree
    	outcome = sm.execute()

   	 # Signal ROS shutdown (kill threads in background)
    	rospy.spin()

	sis.stop()

if __name__ == '__main__':
	main()

