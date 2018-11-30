#  Configure the Kubernetes services on Node

Perform the following steps to configure the kubelet on the node: 

1. Edit /etc/kubernetes/kubelet to appear like this:

    ```
    ###
    # Kubernetes kubelet (node) config
    
    # The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
    KUBELET_ADDRESS="--address=0.0.0.0"
    
    # You may leave this blank to use the actual hostname
    KUBELET_HOSTNAME="--hostname_override=photon-node"
    
    # location of the api-server
    KUBELET_API_SERVER="--api_servers=http://photon-master:8080"
    
    # Add your own
    #KUBELET_ARGS=""
    ```

1. Start the appropriate services on the node (photon-node):

    ```sh
    for SERVICES in kube-proxy kubelet docker; do 
        systemctl restart $SERVICES
        systemctl enable $SERVICES
        systemctl status $SERVICES 
    done
    ```

1. Check to make sure that the cluster can now see the photon-node on photon-master and that its status changes to _Ready_.

   ```console
   kubectl get nodes
   NAME                LABELS              STATUS
   photon-node          name=photon-node-label     Ready
   ```
   
   If the node status is `NotReady`, verify that the firewall rules are permissive for Kubernetes.  
   
   * Deletion of nodes: To delete _photon-node_ from your Kubernetes cluster, one should run the following on photon-master (please do not do it, it is just for information):
   
   ```sh
   kubectl delete -f ./node.json
   ```

## Result

You should have a functional cluster. You can now launch a test pod. For an introduction to working with Kubernetes, see [Kubernetes 101](http://kubernetes.io/docs/user-guide/walkthrough/).



