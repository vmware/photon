# Running a Photon OS Machine on GCE

Photon OS comes in a preconfigured image ready for Google Cloud Engine. 

## Example 

The example in this section shows how to create a Photon OS instance on Google Cloud Engine with and without cloud-init user data.

### Prerequisites 

- You must have set up a GCE account and are ready to pay Google for its cloud services. The GCE-ready version of Photon OS is a free image and is free. You can download it without registration from the following Bintray location: `https://bintray.com/vmware/photon/gce/view`

    The GCE-ready image of Photon OS contains packages and scripts that prepare it for the Google cloud to save you time as you implement a compute cluster or develop cloud applications. The GCE-ready version of Photon OS adds the following packages to the [packages installed with the minimal version](https://github.com/vmware/photon/blob/master/common/data/packages_minimal.json): 
	
    ```
    sudo, tar, which, google-daemon, google-startup-scripts, 
	kubernetes, perl-DBD-SQLite, perl-DBIx-Simple, perl, ntp
```

- Verify that you have the `gcloud command-line tool`. 
    For more information see,  [https://cloud.google.com/compute/docs/gcloud-compute](https://cloud.google.com/compute/docs/gcloud-compute).

### Procedure 

1. Use the following commands to create an instance of Photon OS from the Photon GCE image without using cloud-init. In the commands, you must replace `<bucket-name>` with the name of your bucket and the path to the Photon GCE tar file. 
	
    ```
$ gcloud compute instances list
	$ gcloud compute images list
	$ gcloud config list
	$ gsutil mb gs://<bucket-name>
	$ gsutil cp <path-to-photon-gce-image.tar.gz> gs://<bucket-name>/photon-gce.tar.gz
	$ gcloud compute images create photon-gce-image --source-uri gs://<bucket-name>/photon-gce.tar.gz 
	$ gcloud compute instances create photon-gce-vm --machine-type "n1-standard-1" --image photon-gce-image
	$ gcloud compute instances describe photon-gce-vm
```
	 
1. To create a new instance of a Photon OS machine and configure it with a cloud-init user data file, replace the `gcloud compute instances create` command in the example above with the following command. Before running this command, you must upload your user-data file to Google's cloud infrastructure and replace `<path-to-userdata-file>` with its path and file name. 

    ```
    gcloud compute instances create photon-gce-vm --machine-type "n1-standard-1" --image photon-gce-vm --metadata-from-file=user-data=<path-to-userdata-file>
```
     
    You can also add a cloud-init user-data file to an existing instance of a Photon OS machine on GCE: 
	
    ```
gcloud compute instances add-metadata photon-gce-vm --metadata-from-file=user-data=<path-to-userdata-file>
```
