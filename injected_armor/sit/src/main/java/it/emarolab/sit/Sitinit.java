package it.emarolab.sit;

import it.emarolab.amor.owlInterface.OWLReferences;
import it.emarolab.amor.owlInterface.OWLReferencesInterface;
import it.emarolab.sit.owloopDescriptor.SceneClassDescriptor;
import it.emarolab.sit.realObject.*;
import it.emarolab.sit.sceneRepresentation.SceneRepresentation;

import java.util.HashSet;
import java.util.Set;

//starting sit

public class Sitinit {

    OWLReferences ontology_reference;
    //class constructor requires the string of ontology name

    public Sitinit( String ontology_name )
    {
        //get the reference_ontology with name "ontoloy_name"
        ontology_reference=(OWLReferences) OWLReferencesInterface.OWLReferencesContainer.getOWLReferences(ontology_name);
    }

    public void startSit() {
        // suppress aMOR log
        it.emarolab.amor.owlDebugger.Logger.setPrintOnConsole(false);

        // initialise objects
        Set<GeometricPrimitive> objects = new HashSet<>();

        // define objects
        Sphere s = new Sphere(ontology_reference);
        s.shouldAddTime(true);
        s.setCenter(.3f, .3f, .3f);
        s.setRadius(.1f);
        objects.add(s);

        Plane p = new Plane(ontology_reference);
        p.shouldAddTime(true);
        p.setAxis(.5f, .4f, .1f);
        p.setCenter(.3f, .1f, .1f);
        p.setHessian(.5f);
        objects.add(p);

        System.out.println("Object " + objects);

        System.out.println("1 ----------------------------------------------");

        // the SceneRecognition needs a SpatialSimplifier object
        // to semplify the characteristics of the relations during learning
         SpatialSimplifier simplifier = new SpatialSimplifier( objects);
        // create scene and reason for recognition
        SceneRepresentation recognition1 = new SceneRepresentation(simplifier, ontology_reference);


        // if you want the relation to be human friendly again
        simplifier.populateHumanFriendlyRelationSet();
        // and eventually
        simplifier.readObjectSemantics(true);
        objects = simplifier.getObjects();


        System.out.println("Recognised with best confidence: " + recognition1.getRecognitionConfidence() + " should learn? " + recognition1.shouldLearn());
        System.out.println("Best recognised class: " + recognition1.getBestRecognitionDescriptor());
        System.out.println("Other recognised classes: " + recognition1.getSceneDescriptor().getTypeIndividual());

        // learn the new scene if is the case
        if (recognition1.shouldLearn()) {
            System.out.println("Learning.... ");
            recognition1.learn("TestScene");
        }

        System.out.println("2 ----------------------------------------------");

        // check recognition after learning
        System.out.println("Recognised with best confidence: " + recognition1.getRecognitionConfidence() + " should learn? " + recognition1.shouldLearn());
        System.out.println("Best recognised class: " + recognition1.getBestRecognitionDescriptor());
        System.out.println("Other recognised classes: " + recognition1.getSceneDescriptor().getTypeIndividual());

        System.out.println("3 ----------------------------------------------");
        System.out.println("3 ----------------------------------------------");
        System.out.println("3 ----------------------------------------------");

    }
}