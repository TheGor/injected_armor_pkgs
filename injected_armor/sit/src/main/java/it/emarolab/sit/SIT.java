package it.emarolab.sit;


import it.emarolab.amor.owlInterface.OWLReferences;
import it.emarolab.amor.owlInterface.OWLReferencesInterface;
import it.emarolab.sit.sceneRepresentation.FullSceneRepresentation;
import it.emarolab.amor.owlInterface.OWLReferencesInterface.OWLReferencesContainer;
import it.emarolab.sit.owloopDescriptor.*;
import it.emarolab.sit.realObject.*;
import it.emarolab.sit.sceneRepresentation.SceneRepresentation;
import injected_armor_msgs.*;
import it.emarolab.sit.owloopDescriptor.*;
import it.emarolab.amor.owlInterface.SemanticRestriction;
import it.emarolab.owloop.aMORDescriptor.*;
import org.semanticweb.owlapi.model.*;


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



	public void vision(List<String> list_name,List<ListObjects> list){
		// suppress aMOR log
        	it.emarolab.amor.owlDebugger.Logger.setPrintOnConsole( false);	
		
		Set< GeometricPrimitive> objects = new HashSet<>();
		
		for(int i = 0; i < list_name.size();i++){
			if(list_name.get(i).equals("Sphere")){
				Sphere s = new Sphere( empty_scene);
				s.shouldAddTime( true);
				s.setCenter( (float) list.get(i).getSfera().getCentermsg().getXmsg(),
						(float) list.get(i).getSfera().getCentermsg().getYmsg(),
						(float) list.get(i).getSfera().getCentermsg().getZmsg());
				s.setRadius( (float) list.get(i).getSfera().getRadiusmsg());
				objects.add( s);			
			} else if(list_name.get(i).equals("Plane")){
				Plane p = new Plane( empty_scene);
				p.shouldAddTime( true);
				p.setAxis( (float) list.get(i).getPiano().getAxismsg().getAx(),
						(float) list.get(i).getPiano().getAxismsg().getAy(),
						(float) list.get(i).getPiano().getAxismsg().getAz());
				p.setCenter( (float) list.get(i).getPiano().getCentermsg().getXmsg(),
						(float) list.get(i).getPiano().getCentermsg().getYmsg(),
						(float) list.get(i).getPiano().getCentermsg().getZmsg());
				p.setHessian((float) list.get(i).getPiano().getHessianmsg());
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

		//SceneRepresentation recognition1 = new SceneRepresentation( simplifier, empty_scene);
        	FullSceneRepresentation recognition1 = new FullSceneRepresentation( simplifier, empty_scene);

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


		/*
        Set<SceneClassDescriptor> recognitionClasses = recognition2.getSceneDescriptor().buildTypeIndividual();
        for ( SceneClassDescriptor cl1 : recognitionClasses)
            for ( SceneClassDescriptor cl2 : recognitionClasses)
                if ( ! cl1.equals( cl2))
                    System.out.println( " is " + cl1.getInstance().getIRI().getRemainder().get() +
                            " subclass of " + cl2.getInstance().getIRI().getRemainder().get() +"? " + cl1.getSubConcept().contains( cl2.getInstance()));

		*/
        System.out.println("6 ----------------------------------------------");
		System.out.println("Triplets extraction");

		//string ONTO_NAME2= 'ONTO_NEW';
		//OWLReferences ontoRef2 = OWLReferencesInterface.OWLReferencesContainer.newOWLReferenceFromFileWithPellet(
					//ONTO_NAME2, ONTO_FILE, ONTO_IRI, bufferinReasoner: true)
		Set<OWLClass> classes = empty_scene.getSubClassOf( "Scene");
		for(OWLClass cl : classes)
		{
			SceneClassDescriptor classDescriptor = new SceneClassDescriptor(cl, s);
			classDescriptor.readSemantic();

			Set<SceneClassDescriptor> descriptors = classDescriptor.buildSubConcept();
			if( descriptors.size() <= 1) {
				MORAxioms.Restrictions rest = classDescriptor.getDefinitionConcept();
				for (SemanticRestriction r : rest) {
					try {
						SemanticRestriction.ClassRestrictedOnMinObject rp = (SemanticRestriction.ClassRestrictedOnMinObject) r;
						System.err.println("$$$$" + classDescriptor.getGroundInstance() + " " + rp.getCardinality() + " " + rp.getPropertyName() + " " + rp.getValueName());
					} catch (ClassCastException e) {

					}
				}
			} else {
				for(SceneClassDescriptor desc : descriptors){
					System.out.println( "%%%" + desc.getSubConcept() + " is a " + desc.getGround().getGroundInstance());
				}
			}
		}


	}
}
