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
	rospy.loginfo('Executing state LOOK')
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
	rospy.loginfo('Executing state LISTEN')
	self.answer=raw_input("$$$ Do you want to ask something to Me?\n")
	if self.answer == 'yes':
		print('$$$ Ok, i will reply your questions')
		return 'ready'
	else:
		print('$$$ Ok, i wil not reply your questions')
		return 'not_ready'


#definine a general state which evaluates the keyowrd in input and choose the right processing_respoonse
class Processing_response_general(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['processing_1','processing_2','not_processing'],input_keys=['processing_response_general_input_1','processing_response_general_input_2'])

    def execute(self,userdata):
	rospy.loginfo('Executing state PROCESSING_RESPONSE_GENERAL')
	rospy.loginfo(userdata.processing_response_general_input_2)
	rospy.loginfo(type(userdata.processing_response_general_input_2))
	if  len(userdata.processing_response_general_input_2)==0:
		print('$$$ I do not see what you asking me')
		return 'not_processing'
	elif userdata.processing_response_general_input_2[0] == 'scene':
		return 'processing_1'
	elif (userdata.processing_response_general_input_2[0] == 'plane' or userdata.processing_response_general_input_2[0] == 'sphere'):
		return 'processing_2'
	elif len(userdata.processing_response_general_input_2) > 1:
		return 'processing_1'



#defining processing_response for the keyword 'scene' AND for keyword propeerty + object (right, sphere)
class Processing_response_1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['got_it'], input_keys=['processing_response_input_1','processing_response_input_2'])
#here we processing the reuslt of the sparql_query
    def execute(self,userdata):
	rospy.loginfo('Executing state PROCESSING_RESPONSE_1 ')
	#rospy.loginfo('now u got: %s'%userdata.processing_response_input_1)
        #rospy.loginfo('name: %s'%userdata.processing_response_input_2)
        
	#save the response in a tmp variable
	tmp=userdata.processing_response_input_1
	#string manipulation
	for x in tmp:
		#rospy.loginfo('x iniziale %s ',x)
		x=x.replace("p=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("cls=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("{","")
		x=x.replace("}","")
		#x=x.replace(",","")
		#rospy.loginfo('x finale %s ',x)
	#assign manipulated string to a new list
	tmp1=[]
	tmp1.append(x)
	#rospy.loginfo('lista_finale %s ',tmp1)
	#split tmp1 in different senteces ----> ['PlaneisAboveOf','Sphere',.....] 
	#i have 6 string in the variable sentences
	sentences=tmp1[0].split(',')
	#rospy.loginfo('la mia frase %s ', sentences)
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
	#rospy.loginfo('la mia frase diventa %s ', sentences)		
	#try to build the final sentence
	final_sentences=[]
	j=0
	for i in range(len(sentences)/2):
		s=sentences[j]+" "+sentences[j+1]
		final_sentences.append(s)
		j=j+2
	for z in final_sentences:
		print('$$$ '+z)
	return 'got_it' 

#defining processing_response for the keyword 'plane' or 'sphere'
class Processing_response_2(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['got_it'], input_keys=['processing_response_input_1','processing_response_input_2'])
#here we processing the reuslt of the sparql_query
    def execute(self,userdata):
	#rospy.loginfo('now u got: %s'%userdata.processing_response_input_1)
        #rospy.loginfo('name: %s'%userdata.processing_response_input_2)
        rospy.loginfo('Executing state PROCESSING_RESPONSE_2')
	#save the response in a tmp variable
	tmp=userdata.processing_response_input_1
	#string manipulation
	for x in tmp:
		#rospy.loginfo('x iniziale %s ',x)
		x=x.replace("p=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("cls=http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#","")
		x=x.replace("{","")
		x=x.replace("}","")
		x=x.replace("isBehindOf","")
		x=x.replace("isRightOf","")
		x=x.replace("isLeftOf","")
		x=x.replace("isInFrontOf","")
		x=x.replace("isAboveOf","")
		#rospy.loginfo('x finale %s ',x)
	tmp1=[]
	tmp1.append(x)
	print('$$$ I see a '+tmp1[0])
	return 'got_it'
"""
class Processing_response_3(smach.State):
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
"""

	


def main():
	rospy.init_node('state_machine_robot')

	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['succeeded','preempted','aborted'])	
	sm.userdata.sm_case=0
	sm.userdata.output=""
	sm.userdata.keyword=[]
	
	with sm:
		#define function for loading an ontology, with armorDirectiveSrv
		def set_ontology_request_cb(userdata,request):
			rospy.loginfo('Executing state LOAD_ONTOLOGY')
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
			rospy.loginfo('Executing state INIT_SIT')
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
			rospy.loginfo('Executing state LOOK_SCENE')
			scene_request = ArmorObjectsRequest()
			if sm.userdata.sm_case==1:
				#scene 1 definition
				objects1= ListObjects()
				objects2= ListObjects()
				object1 = SphereMSG()
				object2 = PlaneMSG()
				#Definition Sphere
				object1.radiusmsg = 0.1
				object1.centermsg.xmsg = 5.0
				object1.centermsg.ymsg = 5.0
				object1.centermsg.zmsg = 5.0
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
				#Definition Sphere
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
				object1.radiusmsg = 1.0
				object1.centermsg.xmsg = 15.0
				object1.centermsg.ymsg = 15.0
				object1.centermsg.zmsg = 15.0
				#Definition Sphere
				object2.radiusmsg = 1.0
				object2.centermsg.xmsg = 10.0
				object2.centermsg.ymsg = 10.0
				object2.centermsg.zmsg = 10.0
				#Definition Plane
				object3.hessianmsg = 0.5
				object3.centermsg.xmsg = 4.0
				object3.centermsg.ymsg = 4.0
				object3.centermsg.zmsg = 4.0
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
		smach.StateMachine.add('LISTEN',Listen(),transitions={'ready':'QUERY', 'not_ready':'CLEAN_ONTOLOGY'})


		#define function for querying a robot
		def query_request_cb(userdata,request):
			rospy.loginfo('Executing state QUERY')
			#query_request = ArmorDirectiveRequest()
			#keys_word = ['scene','sphere','plane','above','below','right','left','front','behind']
			query_string='PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX sit: <http://www.semanticweb.org/emaroLab/luca-buoncompagni/sit#> SELECT ?p ?cls WHERE { sit:TestScene (owl:equivalentClass|(owl:intersectionOf/rdf:rest*/rdf:first))* ?restriction . ?restriction owl:minQualifiedCardinality ?min . '
			#query_name=[]
			#question
			query_name=raw_input('$$$ I am ready to answer your question\n'+'**(insert your question by putting a space beetween each word (question mark included))**\n')
			#question string manipulation
			list_phrase_keyword = []
			list_phrase_keyword = query_name.split()
			list_keyword = []
			for x in list_phrase_keyword:
				if x == "scene":
					list_keyword.append(x)
				elif (x == "sphere" or x == "plane"):
					list_keyword.append(x)
				elif (x == "above" or x == "below" or x == "right" or x == "left" or x == "front" or x == "behind"):
					list_keyword.append(x)
			#if we dont have the predicted keyword
			if len(list_keyword)==0 :
				print('michele schifo')
				return request
			#assign list_keyword to userdata for propagating through states 
			userdata.query_output_1=list_keyword
			#print all the keywords
			#for y in sm.userdata.keyword:
				#rospy.loginfo('%s',y)
			#if the keyword list contains 'scene' we compose a specific query
			if list_keyword[0] == "scene":
				request.armor_request.client_name = "client"
				request.armor_request.reference_name = "reference"
				request.armor_request.command = "QUERY"
				request.armor_request.primary_command_spec="SPARQL"
				request.armor_request.secondary_command_spec=""
				request.armor_request.args=[query_string+' ?restriction owl:onClass ?cls . ?restriction owl:onProperty ?p . }']
				return request	
			#if the keyword_list contains sphere or plane, we compose a specific query
			elif (list_keyword[0] == "sphere" or list_keyword[0] == "plane"):
				request.armor_request.client_name = "client"
				request.armor_request.reference_name = "reference"
				request.armor_request.command = "QUERY"
				request.armor_request.primary_command_spec="SPARQL"
				request.armor_request.secondary_command_spec=""
				request.armor_request.args=[query_string+' {?restriction owl:onProperty ?p . FILTER(regex(str(?p),\"'+list_keyword[0]+'\",\"i\"))} UNION {  ?restriction owl:onClass ?cls . FILTER (regex(str(?cls),\"'+list_keyword[0]+'\",\"i\"))}}  LIMIT 1']
				#rospy.loginfo('%s',request.armor_request.args)
				return request
			#if the keyword_list contains a property and an object, we compose a specific query
			elif (list_keyword[0] == "above" or list_keyword[0] == "below" or list_keyword[0] == "right" or list_keyword[0] == "left" or list_keyword[0] == "front" or list_keyword[0] == "behind" ):
				if (list_keyword[1] == "sphere" or list_keyword[1] == "plane"):
					request.armor_request.client_name = "client"
					request.armor_request.reference_name = "reference"
					request.armor_request.command = "QUERY"
					request.armor_request.primary_command_spec="SPARQL"
					request.armor_request.secondary_command_spec=""
					request.armor_request.args=[query_string+' ?restriction owl:onClass ?cls . ?restriction owl:onProperty ?p . FILTER(regex(str(?p),\"'+list_keyword[0]+'\",\"i\") && regex(str(?cls),\"'+list_keyword[1]+'\",\"i\"))}  ']
				#rospy.loginfo('%s',request.armor_request.args)
				return request


				
		
		def query_response_cb(userdata,response):
			#query_response = ArmorDirectiveResponse()
			#rospy.loginfo('%s', response.armor_response.queried_objects)
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
			smach.StateMachine.add('PROCESSING_RESPONSE_GENERAL',Processing_response_general(),transitions={'processing_1':'PROCESSING_RESPONSE_1','processing_2':'PROCESSING_RESPONSE_2','not_processing':'done'},remapping={'processing_response_general_input_1':'output','processing_response_general_input_2':'keyword'})
				
			
			#adding state processing_repsonse_1 which process response for keyword scene or for keyword property+object
			smach.StateMachine.add('PROCESSING_RESPONSE_1',Processing_response_1(),transitions={'got_it':'done'},remapping={'processing_response_input_1':'output','processing_response_input_2':'keyword'})

			#adding state processing_repsonse_2 which process response for keyword object (plane or sphere)
			smach.StateMachine.add('PROCESSING_RESPONSE_2',Processing_response_2(),transitions={'got_it':'done'},remapping={'processing_response_input_1':'output','processing_response_input_2':'keyword'})			

			#adding state processing_repsonse_3 which process response for keyword property and object (right, sphere)
			#smach.StateMachine.add('PROCESSING_RESPONSE_3',Processing_response_3(),transitions={'got_it':'done'},remapping={'processing_response_input_1':'output','processing_response_input_2':'keyword'})


			
		
		#first state of the submachine		
		smach.StateMachine.add('PROCESSING_RESPONSE',sm1, transitions={'done':'LISTEN'})


		#definition state for clean
		def clean_ontology_request_cb(userdata,request):
			rospy.loginfo('Executing state CLEAN_ONTOLOGY')
			#clean_ontology_request = ArmorDirectiveRequest()
			request.armor_request.client_name = "client"
			request.armor_request.reference_name = "reference"
			request.armor_request.command = "CLEAN"
			request.armor_request.primary_command_spec = ""
			request.armor_request.secondary_command_spec = ""
			#pay attention to the true parameter for adding new individuals
			request.armor_request.args = ['GeometricPrimitive']
			return request
		
		smach.StateMachine.add('CLEAN_ONTOLOGY',smach_ros.ServiceState('armor_interface_srv',ArmorDirective,request_cb = 									clean_ontology_request_cb),transitions={'succeeded':'LOOK'})
		



		


	


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

