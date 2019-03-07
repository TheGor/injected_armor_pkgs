package it.emarolab.armor;

import injected_armor_msgs.*;
import org.ros.node.ConnectedNode;
import it.emarolab.sit.*;
import it.emarolab.armor.ARMORCommandUtility;

import java.util.*;

class ARMORLinkSit {

	private Boolean response;
	private ListObjects request;
	private ConnectedNode connectedNode;
	private String scene_onto;	

	//class that works as a link between sit and armor
	ARMORLinkSit(){
		
	}


	public List<String> AreObjects(List<String> name,List<ListObjects> r){

		//checks if there are objects
		int cont = 0;
		for(int i = 0; i < name.size(); i++){
			if(name.contains("Sphere") || name.contains("Plane")){
				cont++;
			}		
		}
		//if there are objects it create the sit and start vision simulation
		if(cont > 0) {
			//SIT sit = new SIT();
			SIT sit = new SIT();
			//SIT sit = new SIT(getSceneOnto());
			List<String> sceneLooked = sit.vision(name,r);
			return sceneLooked;
		}
		return null;
	}
	/*public boolean IsCone(){
		if(request.getCono() != null){
			return true;		
		}
		return false;	
	}*/
	

	
}
