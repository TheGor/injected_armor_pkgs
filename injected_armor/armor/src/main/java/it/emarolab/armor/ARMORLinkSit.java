package it.emarolab.armor;

import injected_armor_msgs.*;
import org.ros.node.ConnectedNode;
import it.emarolab.sit.*;
import it.emarolab.armor.ARMORCommandUtility;

import java.util.*;

/**
 * This class link ARMOR to SIT
 *
 */

class ARMORLinkSit {

	private Boolean response;
	private ListObjects request;
	private ConnectedNode connectedNode;
	private String scene_onto;	

	//class that works as a link between sit and armor
	ARMORLinkSit(){
		
	}

	/**
	 * checks if there are objects in name object list and if
	 * there are objects,calls sit
	 * @param name : list of obects name
	 * @param r  : list of objects
	 * @return
	 */
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
			List<String> sceneLooked = sit.vision(name,r);
			return sceneLooked;
		}
		return null;
	}

	
}
