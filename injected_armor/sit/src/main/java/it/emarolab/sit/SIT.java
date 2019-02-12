package it.emarolab.sit;

import it.emarolab.amor.owlInterface.OWLReferences;
import it.emarolab.amor.owlInterface.OWLReferencesInterface;
import it.emarolab.amor.owlInterface.OWLReferencesInterface.OWLReferencesContainer;
import it.emarolab.sit.owloopDescriptor.SceneClassDescriptor;
import it.emarolab.sit.realObject.*;
import it.emarolab.sit.sceneRepresentation.SceneRepresentation;
import injected_armor_msgs.*;

import java.util.HashSet;
import java.util.Set;
import java.util.*;

// sit class
// the second client starts the sit (you should see "SIT ACTIVE" in your terminal
//then the third client pass to sit all the object's features
// it also ececute the reasiing

public class SIT {

	OWLReferences empty_scene;
	public static String s;
	

	public SIT(){
		empty_scene = (OWLReferences) OWLReferencesInterface.OWLReferencesContainer.getOWLReferences(s);
	}



	public void vision(List<String> list_name,ListObjects list){
		// suppress aMOR log
        	it.emarolab.amor.owlDebugger.Logger.setPrintOnConsole( false);	
		
		Set< GeometricPrimitive> objects = new HashSet<>();
		
		for(int i = 0; i < list_name.size();i++){
			if(list_name.get(i).equals("Sphere")){
				Sphere s = new Sphere( empty_scene);
				s.shouldAddTime( true);
				s.setCenter( (float) list.getSfera().getCentermsg().getXmsg(), (float) list.getSfera().getCentermsg().getYmsg(), (float) list.getSfera().getCentermsg().getZmsg());
				s.setRadius( (float) list.getSfera().getRadiusmsg());
				objects.add( s);			
			} else if(list_name.get(i).equals("Plane")){
				Plane p = new Plane( empty_scene);
				p.shouldAddTime( true);
				p.setAxis( (float) list.getPiano().getAxismsg().getAx(), (float) list.getPiano().getAxismsg().getAy(), (float) list.getPiano().getAxismsg().getAz());
				p.setCenter( (float) list.getPiano().getCentermsg().getXmsg(), (float) list.getPiano().getCentermsg().getYmsg(), (float) list.getPiano().getCentermsg().getZmsg());
				p.setHessian((float) list.getPiano().getHessianmsg());
				objects.add( p);			
			}		
		}
 
		/*Sphere s = new Sphere( empty_scene);
		s.shouldAddTime( true);
		s.setCenter( .3f, .3f, .3f);
		s.setRadius( .1f);
		objects.add( s);

		Plane p = new Plane( empty_scene);
		p.shouldAddTime( true);
		p.setAxis( .5f, .4f, .1f);
		p.setCenter( .3f, .1f, .1f);
		p.setHessian( .5f);
		objects.add( p);*/

		System.out.println( "Object " + objects);

		System.out.println("1 ----------------------------------------------");

		SpatialSimplifier simplifier = new SpatialSimplifier( objects);

		SceneRepresentation recognition1 = new SceneRepresentation( simplifier, empty_scene);

		System.out.println( "Recognised with best confidence: " + recognition1.getRecognitionConfidence() + " should learn? " + recognition1.shouldLearn());
		System.out.println( "Best recognised class: " + recognition1.getBestRecognitionDescriptor());
		System.out.println( "Other recognised classes: " + recognition1.getSceneDescriptor().getTypeIndividual());

		// learn the new scene if is the case
		if ( recognition1.shouldLearn()) {
		    System.out.println("Learning.... ");
		    recognition1.learn("TestScene");
		}

		System.out.println("2 ----------------------------------------------");

		// check recognition after learning
		System.out.println( "Recognised with best confidence: " + recognition1.getRecognitionConfidence() + " should learn? " + recognition1.shouldLearn());
		System.out.println( "Best recognised class: " + recognition1.getBestRecognitionDescriptor());
		System.out.println( "Other recognised classes: " + recognition1.getSceneDescriptor().getTypeIndividual());

		System.out.println("3 ----------------------------------------------");
		System.out.println("3 ----------------------------------------------");
		System.out.println("3 ----------------------------------------------");

	}


	


}
