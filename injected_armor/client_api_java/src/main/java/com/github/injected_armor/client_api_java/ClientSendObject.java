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
    object_seen.add("Sphere");
    object_seen.add("Plane");
    /*float coord_x = 0.3f;
    float coord_y = 0.3f;
    float coord_z = 0.3f;
    float radius = 0.1f;  */
    //set the request/size

    //request.setSize(10);
    request.setNameObject(object_seen);
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
