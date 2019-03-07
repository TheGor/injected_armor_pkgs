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


//client that simulate pit

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

    List<String> object_seen = new ArrayList<String>();

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
        	connectedNode.getLog().info(response.getSceneName());
      }

      @Override
      public void onFailure(RemoteException e) {
        throw new RosRuntimeException(e);
      }
    });
  }
}
