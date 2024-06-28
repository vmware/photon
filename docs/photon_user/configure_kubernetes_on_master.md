# Configure Kubernetes Services on the Master

Perform the following steps to configure Kubernetes services on the master:

1. Edit `/etc/kubernetes/apiserver` to appear as such.  The `service_cluster_ip_range` IP addresses must be an unused block of addresses, not used anywhere else.  They do not need to be routed or assigned to anything.

    ```
    # The address on the local server to listen to.
    KUBE_API_ADDRESS="--address=0.0.0.0"
    
    # Comma separated list of nodes in the etcd cluster
    KUBE_ETCD_SERVERS="--etcd_servers=http://127.0.0.1:4001"
    
    # Address range to use for services
    KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"
    
    # Add your own
    KUBE_API_ARGS=""
    ```

1. Start the appropriate services on master:

    ```
    for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler; do
    	systemctl restart $SERVICES
    	systemctl enable $SERVICES
    	systemctl status $SERVICES
    done
    ```

1. To add the other node, create the following `node.json` file on the Kubernetes master node:

    ```json
    {
        "apiVersion": "v1",
        "kind": "Node",
        "metadata": {
            "name": "photon-node",
            "labels":{ "name": "photon-node-label"}
        },
        "spec": {
            "externalID": "photon-node"
        }
    }
    ```
    
1. Create a node object internally in your Kubernetes cluster by running the following command:
    
    ```console
    $ kubectl create -f ./node.json
    
    $ kubectl get nodes
    NAME                LABELS              STATUS
    photon-node         name=photon-node-label     Unknown
    ```

**Note**: The above example only creates a representation for the node `photon-node` internally. It does not provision the actual `photon-node`. Also, it is assumed that `photon-node` (as specified in `name`) can be resolved and is reachable from the Kubernetes master node. 