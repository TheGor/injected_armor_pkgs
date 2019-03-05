package com.github.rosjava.injected_armor.client_api_java;

import org.ros.exception.RemoteException;
import org.ros.exception.RosRuntimeException;
import org.ros.exception.ServiceNotFoundException;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.service.ServiceClient;
import org.ros.node.service.ServiceResponseListener;
import injected_armor_msgs.*;
import java.util.*;

/**
 * A simple {@link Publisher} {@link NodeMain}.
 */

//a client (third client) that send objects to sit by passing through armor
  //it uses messages and service defined in armormsgpkg
  //set all the data
  //there are a message for a center and axis
  //then the are messages for objects sphere,plane (that contains center and axis)
  //and finally a message with both objects (da cambiare)
  //the service is composed by an arraylist of strings that contains obect's name
  //and the message that contains two object

  //we need to modify this client

  //################################################################################
  //################################################################################

  //we modified the service and changed thing of type "listObject" from a simple variable to an array
  // so we modified this client for using this servicd

public class ClientSendObject extends AbstractNodeMain {
  @Override
  public GraphName getDefaultNodeName() {
    return GraphName.of("rosjava/clientsendobject");
  }

  @Override
  public void onStart(final ConnectedNode connectedNode) {
    ServiceClient<ArmorObjectsRequest, ArmorObjectsResponse> serviceClient;
    try {
      serviceClient = connectedNode.newServiceClient("send_objects", ArmorObjects._TYPE);
    } catch (ServiceNotFoundException e) {
      throw new RosRuntimeException(e);
    }
    final ArmorObjectsRequest request = serviceClient.newMessage();
    //first client
    /*List<String> object_seen = new ArrayList<String>();
    object_seen.add("Sphere");
    object_seen.add("Plane");
    /*float coord_x = 0.3f;
    float coord_y = 0.3f;
    float coord_z = 0.3f;
    float radius = 0.1f;  */
    //set the request/size

    //request.setSize(10);
    /*request.setNameObject(object_seen);
    request.getThing().getSfera().getCentermsg().setXmsg(0.3);
    request.getThing().getSfera().getCentermsg().setYmsg(0.3);
    request.getThing().getSfera().getCentermsg().setZmsg(0.3);
    request.getThing().getSfera().setRadiusmsg(0.1);
    request.getThing().getPiano().getCentermsg().setXmsg(0.8);
    request.getThing().getPiano().getCentermsg().setYmsg(0.8);
    request.getThing().getPiano().getCentermsg().setZmsg(0.8);
    request.getThing().getPiano().getAxismsg().setAx(0.5);
    request.getThing().getPiano().getAxismsg().setAy(0.5);
    request.getThing().getPiano().getAxismsg().setAz(0.5);
    request.getThing().getPiano().setHessianmsg(0.6);
    */

    //client modfied
    //an arraylist with all objet names., we need to fill it and then pass it to the arraylist of names
    //defined in the request
    List<String> object_seen = new ArrayList<String>();
    //now we create a list of injected_Armor msgs, we need it to create different scenes
    /* nell' arraylist  allobjects voglio avere un array in cui ogni cella ha al proprio
    interno gli oggetti che voglio aggiungere alla scena. Ogni cella avrà tutti gli oggetti ma poi decido di
    settarne solo uno. Cosi in ogni cella dell'array ho solo un oggeto.
    L'array stesso nel totale sarà la scena
    */
    List<injected_armor_msgs.ListObjects> all_objects = new ArrayList<>();
    //every of the following istruction creates a new cell of the list defined above
    //we create 3 different cell for 3 object
    injected_armor_msgs.ListObjects object_1 = connectedNode.getTopicMessageFactory().newFromType(injected_armor_msgs.ListObjects._TYPE);
    injected_armor_msgs.ListObjects object_2 = connectedNode.getTopicMessageFactory().newFromType(injected_armor_msgs.ListObjects._TYPE);
    injected_armor_msgs.ListObjects object_3 = connectedNode.getTopicMessageFactory().newFromType(injected_armor_msgs.ListObjects._TYPE);

    //we define a randm number for picking one of 3 different scenes
    Random r = new Random();
    int num_random = r.nextInt(4-1)+1;

    //we defined 3 different scenes
    //in each scene we define object

    switch(num_random){
      case 1:
        //scene composed by two sphere
        object_seen.add("Sphere");
        object_seen.add("Sphere");


        //we defined the first sphere in the first cell of the array
        object_1.getSfera().setRadiusmsg(1.5);
        object_1.getSfera().getCentermsg().setXmsg(15.0);
        object_1.getSfera().getCentermsg().setYmsg(15.0);
        object_1.getSfera().getCentermsg().setZmsg(15.0);
        //we defined second sphere in the second cell of the array
        object_2.getSfera().setRadiusmsg(1.5);
        object_2.getSfera().getCentermsg().setXmsg(10.0);
        object_2.getSfera().getCentermsg().setYmsg(10.0);
        object_2.getSfera().getCentermsg().setZmsg(10.0);
        //we add it to the arraylist
        all_objects.add(object_1);
        all_objects.add(object_2);

        break;
       //scene with one sphere and a plane
      case 2:
        object_seen.add("Sphere");
        object_seen.add("Plane");

        object_1.getSfera().setRadiusmsg(1.5);
        object_1.getSfera().getCentermsg().setXmsg(5.0);
        object_1.getSfera().getCentermsg().setYmsg(5.0);
        object_1.getSfera().getCentermsg().setZmsg(5.0);

        object_2.getPiano().getCentermsg().setXmsg(0.5);
        object_2.getPiano().getCentermsg().setYmsg(0.5);
        object_2.getPiano().getCentermsg().setZmsg(0.5);
        object_2.getPiano().getAxismsg().setAx(0.5);
        object_2.getPiano().getAxismsg().setAy(0.5);
        object_2.getPiano().getAxismsg().setAz(0.5);
        object_2.getPiano().setHessianmsg(0.5);

        all_objects.add(object_1);
        all_objects.add(object_2);
        break;
        //scene 3, two sphere and one plane
      case 3:
        object_seen.add("Sphere");
        object_seen.add("Sphere");
        object_seen.add("Plane");

        object_1.getSfera().setRadiusmsg(1.5);
        object_1.getSfera().getCentermsg().setXmsg(20.0);
        object_1.getSfera().getCentermsg().setYmsg(20.0);
        object_1.getSfera().getCentermsg().setZmsg(20.0);

        object_2.getSfera().setRadiusmsg(1.5);
        object_2.getSfera().getCentermsg().setXmsg(25.0);
        object_2.getSfera().getCentermsg().setYmsg(25.0);
        object_2.getSfera().getCentermsg().setZmsg(25.0);

        object_3.getPiano().getCentermsg().setXmsg(1.0);
        object_3.getPiano().getCentermsg().setYmsg(1.0);
        object_3.getPiano().getCentermsg().setZmsg(1.0);
        object_3.getPiano().getAxismsg().setAx(1.0);
        object_3.getPiano().getAxismsg().setAy(1.0);
        object_3.getPiano().getAxismsg().setAz(1.0);
        object_3.getPiano().setHessianmsg(1.0);

        all_objects.add(object_1);
        all_objects.add(object_2);
        all_objects.add(object_3);
        break;
    }

    request.setThing(all_objects);
    request.setNameObject(object_seen);

    serviceClient.call(request, new ServiceResponseListener<ArmorObjectsResponse>() {
      @Override
      public void onSuccess(ArmorObjectsResponse response) {
        	connectedNode.getLog().info(String.format("The response is : "));
		/*connectedNode.getLog().info(response.getCex());
		connectedNode.getLog().info(response.getCey());
		connectedNode.getLog().info(response.getCez());
		connectedNode.getLog().info(response.getRad());*/
		connectedNode.getLog().info(response.getStatus());
      }

      @Override
      public void onFailure(RemoteException e) {
        throw new RosRuntimeException(e);
      }
    });
  }
}
