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
        smach.State.__init__(self, outcomes=['succeeded','failed'],output_keys=['look_case_in'])
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
	time.sleep(30)
	if self.one_received:
		userdata.look_case_in=1
	elif self.two_received:
		userdata.look_case_in=2
	elif self.three_received:
		userdata.look_case_in=3
	else:
		return 'failed'
	return 'succeeded'
	

def main():
	rospy.init_node('state_machine_robot')

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['succeeded','preempted','aborted'])	
	sm.userdata.sm_case=0
	
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
		smach.StateMachine.add('LOOK',Look(),transitions={'succeeded':'LOOK_SCENE',
									'failed': 'aborted'},remapping={'look_case_in':'sm_case'}) 


		#define function for passing object data
		def scene_request_cb(userdata,request):
			scene_request = ArmorObjectsRequest()
			if sm.userdata.sm_case==1:
				#scene 1 definition
				objects1= ListObjects()
				objects2= ListObjects()
				object1 = SphereMSG()
				object2 = PlaneMSG()
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
				scene_request.thing = [objects1,objects2]
				scene_request.name_object = ["Sphere","Plane"]
			
			
			elif sm.userdata.sm_case==2:
				#scene 2 definition
				objects1= ListObjects()
				objects2= ListObjects()
				object1 = SphereMSG()
				object2 = SphereMSG()
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
				scene_request.thing = [objects1,objects2]
				scene_request.name_object = ["Sphere","Sphere"]
			
			
			elif sm.userdata.sm_case==3:
				#scene 3 definition
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
				scene_request.thing = [objects1,objects2,objects3]
				scene_request.name_object = ["Sphere","Sphere","Plane"]
			
			return scene_request
			
	
				
		
		
		#define scene state
		smach.StateMachine.add('LOOK_SCENE',smach_ros.ServiceState('send_objects',ArmorObjects,request_cb = 									scene_request_cb),transitions={'succeeded':'succeeded'})


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

