---
title:  Installing Photon OS on Google Compute Engine
weight: 2
---

You can use either the Google Cloud Platform or the gcloud CLI to upload the Photon OS GCE tar file to the bucket, and create the Image & Photon OS VM instance.

## Setting Up Using the Google Cloud Platform

After you download the Photon OS image for GCE, log into GCE and install Photon OS. 

Perform the following steps:

1. Create a New Bucket

    Create a new bucket to store your Photon OS image for GCE.
    
    ![gce1](./installation-guide/images/gce1.jpg)

1. Upload the Photon OS Image

    While viewing the bucket that created, click the `Upload files` button, navigate to your Photon OS image and click the `Choose` button. 
    
    When the upload finishes, you can see the Photon OS compressed image in the file list for the bucket that you created.
    
    ![gce2](./installation-guide/images/gce2.jpg)

1. Create a New Image

    To create a new image, click on `Images` in the `Compute` category in the left panel and then click on the `New Image` button. 
    
    Enter a name for the image in the `Name` field and change the `Source` to `Cloud Storage file` using the pull-down menu. Then, in the `Cloud Storage file` field, enter the bucket name and filename as the path to the Photon OS image for GCE. In this example, where the bucket was named `photon_storage,` the path is as follows:
     
    	`photon_storage/photon-gce-2.0-tar.gz`
    
    The new image form autopopulates the `gs://` file path prefix.*
    
    Click the `Create` button to create your image. You must be able to see the Images catalog and your Photon OS image at the top of the list. 

1. Create a New Instance

    To create an instance, check the box next to the Photon OS image and click the `Create Instance` button. 
    
    On the `Create a new instance` form, provide a name for this instance, confirm the zone into which this instance is to be deployed and, before clicking `Create,` check the `Allow HTTP traffic` and `Allow HTTPS traffic` options. 
    
    **Note**: The firewall rules in this example are optional. You can configure the ports according to your requirements. 
    
    ![gce4](./installation-guide/images/gce4.jpg)
    
    When the instance is created you will be returned to your list of VM instances. If you click on the instance, the status page for the instance will allow you to SSH into your Photon OS environment using the SSH button at the top of the panel. 
    
    At this point, your instance is running and you are ready to start the Docker engine and run a container workload. For more information, see [Deploying a Containerized Application in Photon OS](./installation-guide/deploying-a-containerized-application-in-photon-os/).


## Setting Up Using the gcloud CLI
​
**Example Setup Script:**   
​
You can use the following script (create.sh) to upload your tar file programmatically to the bucket and create the VM.
​
```
#!/bin/bash
timestamp=$(date +%s)
export PATH=$PATH:/root/gce/google-cloud-sdk/bin
​
# get branch name in order to determine the machine type.
GCE_VM_NAME=$2
branch=`echo ${GCE_VM_NAME} | cut -d '-' -f 1`
​
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GCE_USERNAME=<gce_username>
GCE_BUCKET=<gs://bucket-name>
​
if [ $# -lt 2 ]
then
  echo "Usage is: create.sh <path_to_gce_image.tar.gz> <vm_name> [(optional) <user-data-file-path>]";
  exit;
fi
​
echo "Uploading gce tar.gz to gce bucket...."
/root/gce/google-cloud-sdk/bin/gsutil cp ${1} $GCE_BUCKET/photon-gce-${timestamp}.tar.gz
if [ ! "$?" -eq 0 ]; then
    echo "Failed: couldn't upload to gce bucket"
    exit 1
fi
​
echo "GCE tar.gz uploaded successfully, proceeding with image creation"
gcloud compute images create ${2}-image --source-uri $GCE_BUCKET/photon-gce-${timestamp}.tar.gz
if [ ! "$?" -eq 0 ]; then
    echo "Failed: couldn't create image successfully"
    exit 1
fi
​
echo "GCE image created successfully. Proceeding with instance creation"
if [[ ( "${branch}" != "one" ) && ( "${branch}" != "two" ) ]];then
    machine_type="n1-standard-1"
else
    machine_type="n1-standard-2"
fi
echo branch=$branch
echo machine_type=$machine_type
​
if [ $# -gt 2 ]
then
    gcloud compute instances create ${2} --machine-type ${machine_type} --image ${2}-image --metadata-from-file=user-data=${3}
else
    gcloud compute instances create ${2} --machine-type ${machine_type} --image ${2}-image
fi
if [ ! "$?" -eq 0 ]; then
    echo "Failed: couldn't create instance successfully"
    exit 1
fi
echo "Photon Instance created successfully on GCE"
​
externalip="$(gcloud compute instances list ${2} --format='value(networkInterfaces[].accessConfigs[].natIP)')"
echo $externalip
GCE_VM_IP=$externalip
echo GCE_VM_IP=$GCE_VM_IP
```   