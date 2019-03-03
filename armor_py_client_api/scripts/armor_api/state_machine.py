#!/usr/bin/env python

import rospy
import smach
import smach_ros
import injected_armor_msgs.srv
from injected_armor_msgs.srv import ArmorDirective,ArmorDirectiveRequest,ArmorObjects,ArmorObjectsRequest,ArmorDirectiveResponse
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
	#This declares that your node subscribes to the chatter topic which is of type Int16. When new messages are received, 		      		#callback is invoked with the message as the first argument.
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
	time.sleep(15)
	if self.one_received:
		userdata.look_case_in=1
	elif self.two_received:
		userdata.look_case_in=2
	elif self.three_received:
		userdata.look_case_in=3
	else:
		return 'failed'
	return 'succeeded'
	
class Listen(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['ready','not_ready'])

    def execute(self,userdata):
	rospy.loginfo('Executing state Listen')
	self.answer=raw_input("Do you want to ask something to Me?\n")
	if self.answer == 'yes':
		return 'ready'
	else:
		return 'not_ready'


#definine a general state which evaluates the keyowrd in input and choose the right processing_respoonse
class Processing_response_general(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['processing_1','processing_2'],input_keys=['processing_response_general_input_1','processing_response_general_input_2'])

    def execute(self,userdata):
	rospy.loginfo('Executing state Processing Response General')
	rospy.loginfo(userdata.processing_response_general_input_2)
	if userdata.processing_response_general_input_2 == 'scene':
		rospy.loginfo('michele maiale')
		return 'processing_1'
	elif (userdata.processing_response_general_input_2 == 'plane' or userdata.processing_response_general_input_2 == 'sphere'):
		return 'processing_2'
	#elif userdata.processing_response_general_input_1 == 'michele':
	#	return 'processing_3'


#defining processing_response for the keyword 'scene'
class Processing_response_1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['got_it'], input_keys=['processing_response_input_1','processing_response_input_2'])
#here we processing the reuslt of the sparql_query
    def execute(self,userdata):
	rospy.loginfo('Executing state ')
	rospy.loginfo('now u got: %s'%userdata.processing_response_input_1)
        rospy.loginfo('name: %s'%userdata.processing_response_input_2)
        
	#save the response in a tmp variable
	tmp=userdata.processing_response_input_1
	#string manipulation
	for x in tmp:
		rospy.loginfo('x iniziale %s ',x)
		x=x.replace("p=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("cls=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("{","")
		x=x.replace("}","")
		#x=x.replace(",","")
		rospy.loginfo('x finale %s ',x)
	#assign manipulated string to a new list
	tmp1=[]
	tmp1.append(x)
	rospy.loginfo('lista_finale %s ',tmp1)
	#split tmp1 in different senteces ----> ['PlaneisAboveOf','Sphere',.....] 
	#i have 6 string in the variable sentences
	sentences=tmp1[0].split(',')
	rospy.loginfo('la mia frase %s ', sentences)
	#more working, trying to separate Plane/is/Above/Of
	for k in range(len(sentences)):
		if k % 2==0:
			if('Plane' in sentences[k]):
				sentences[k]=sentences[k].replace('Plane','Plane ')
				if('Behind' in sentences[k]):
					sentences[k]=sentences[k].replace('Behind',' Behind ')
				elif('Above' in sentences[k]):
					sentences[k]=sentences[k].replace('Above',' Above ')
				elif('Right' in sentences[k]):
					sentences[k]=sentences[k].replace('Right',' Right ')
				elif('Left' in sentences[k]):
					sentences[k]=sentences[k].replace('Left',' Left ')
				elif('InFront' in sentences[k]):
					sentences[k]=sentences[k].replace('InFront',' In Front ')
			elif('Sphere' in sentences[k]):
				sentences[k]=sentences[k].replace('Sphere','Sphere ')
				if('Behind' in sentences[k]):
					sentences[k]=sentences[k].replace('Behind',' Behind ')
				elif('Above' in sentences[k]):
					sentences[k]=sentences[k].replace('Above',' Above ')
				elif('Right' in sentences[k]):
					sentences[k]=sentences[k].replace('Right',' Right ')
				elif('Left' in sentences[k]):
					sentences[k]=sentences[k].replace('Left',' Left ')
				elif('InFront' in sentences[k]):
					sentences[k]=sentences[k].replace('InFront',' In Front ')
	rospy.loginfo('la mia frase diventa %s ', sentences)		
	#try to build the final sentence
	final_sentences=[]
	j=0
	for i in range(len(sentences)/2):
		s=sentences[j]+" "+sentences[j+1]
		final_sentences.append(s)
		j=j+2
	for z in final_sentences:
		rospy.loginfo('%s', z)
	return 'got_it' 

#defining processing_response for the keyword 'plane' or 'sphere'
class Processing_response_2(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['got_it'], input_keys=['processing_response_input_1','processing_response_input_2'])
#here we processing the reuslt of the sparql_query
    def execute(self,userdata):
	rospy.loginfo('now u got: %s'%userdata.processing_response_input_1)
        rospy.loginfo('name: %s'%userdata.processing_response_input_2)
        
	#save the response in a tmp variable
	tmp=userdata.processing_response_input_1
	#string manipulation
	for x in tmp:
		rospy.loginfo('x iniziale %s ',x)
		x=x.replace("p=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("cls=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("{","")
		x=x.replace("}","")
		x=x.replace("isBehindOf","")
		x=x.replace("isRightOf","")
		x=x.replace("isLeftOf","")
		x=x.replace("isInFrontOf","")
		x=x.replace("isAboveOf","")
		rospy.loginfo('x finale %s ',x)
	tmp1=[]
	tmp1.append(x)
	rospy.loginfo('frase_finale : %s ','I see a '+tmp1[0])
	return 'got_it'

	


def main():
	rospy.init_node('state_machine_robot')

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['succeeded','preempted','aborted'])	
	sm.userdata.sm_case=0
	sm.userdata.output=""
	sm.userdata.keyword=""
	
	with sm:
		#define function for loading an ontology, with armorDirectiveSrv
		def set_ontology_request_cb(userdata,request):
			set_ontology_request = ArmorDirectiveRequest()
			set_ontology_request.armor_request.client_name = "client"
			set_ontology_request.armor_request.reference_name = "reference"
			set_ontology_request.armor_request.command = "LOAD"
			set_ontology_request.armor_request.primary_command_spec = "FILE"
			set_ontology_request.armor_request.secondary_command_spec = ""
			#pay attention to the true parameter for adding new individuals
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
		smach.StateMachine.add('LOOK_SCENE',smach_ros.ServiceState('send_objects',ArmorObjects,request_cb = 									scene_request_cb),transitions={'succeeded':'LISTEN'})

		#define state listen
		smach.StateMachine.add('LISTEN',Listen(),transitions={'ready':'QUERY', 'not_ready':'aborted'})


		#define function for querying a robot
		def query_request_cb(userdata,request):
			#query_request = ArmorDirectiveRequest()
			query_string='PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX sit: <http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#> SELECT ?p ?cls WHERE { sit:TestScene (owl:equivalentClass|(owl:intersectionOf/rdf:rest*/rdf:first))* ?restriction . ?restriction owl:minQualifiedCardinality ?min . '
			query_name=raw_input('prototipo di domanda\n')
			#first type of question
			rospy.loginfo(type(query_name))
			userdata.query_output_1=query_name
			rospy.loginfo('%s',sm.userdata.keyword)
			if(query_name=='scene'):
				request.armor_request.client_name = "client"
				request.armor_request.reference_name = "reference"
				request.armor_request.command = "QUERY"
				request.armor_request.primary_command_spec="SPARQL"
				request.armor_request.secondary_command_spec=""
				request.armor_request.args=[query_string+' ?restriction owl:onClass ?cls . ?restriction owl:onProperty ?p . }']
				return request
			#second type of question
			if(query_name=='sphere' or query_name=='plane'):
				request.armor_request.client_name = "client"
				request.armor_request.reference_name = "reference"
				request.armor_request.command = "QUERY"
				request.armor_request.primary_command_spec="SPARQL"
				request.armor_request.secondary_command_spec=""
				request.armor_request.args=[query_string+' {?restriction owl:onProperty ?p . FILTER(regex(str(?p),\"'+query_name+'\",\"i\"))} UNION {  ?restriction owl:onClass ?cls . FILTER (regex(str(?cls),\"'+query_name+'\",\"i\"))}}  LIMIT 1']
				rospy.loginfo('%s',request.armor_request.args)
				return request
		#define function query result processing
		def query_response_cb(userdata,response):
			#query_response = ArmorDirectiveResponse()
			rospy.loginfo('%s', response.armor_response.queried_objects)
			#rospy.loginfo('%s', sm.userdata.keyword)
			userdata.query_output=response.armor_response.queried_objects
			return 'succeeded';

		#adding state for query
		smach.StateMachine.add('QUERY',smach_ros.ServiceState('armor_interface_srv',ArmorDirective,request_cb = 									query_request_cb,response_cb=query_response_cb,output_keys=['query_output','query_output_1']),transitions={'succeeded':'PROCESSING_RESPONSE'},remapping={'query_output':'output','query_output_1':'keyword'})

		#create a substate machine which contains the processing of the response
		
        	sm1 = smach.StateMachine(outcomes=['done'],input_keys=['output','keyword'])
		#sm1.userdata.output_submachine = ''
		#define Processing_response state
		with sm1:
			#adding state processing general
			smach.StateMachine.add('PROCESSING_RESPONSE_GENERAL',Processing_response_general(),transitions={'processing_1':'PROCESSING_RESPONSE_1','processing_2':'PROCESSING_RESPONSE_2'},remapping={'processing_response_general_input_1':'output','processing_response_general_input_2':'keyword'})
				
			
			#adding state processing_repsonse_1 which process response for keyword scene
			smach.StateMachine.add('PROCESSING_RESPONSE_1',Processing_response_1(),transitions={'got_it':'done'},remapping={'processing_response_input_1':'output','processing_response_input_2':'keyword'})

			#adding state processing_repsonse_2 which process response for keyword scene
			smach.StateMachine.add('PROCESSING_RESPONSE_2',Processing_response_2(),transitions={'got_it':'done'},remapping={'processing_response_input_1':'output','processing_response_input_2':'keyword'})
		
		#first state of the submachine		
		smach.StateMachine.add('PROCESSING_RESPONSE',sm1, transitions={'done':'succeeded'})



		


	


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

