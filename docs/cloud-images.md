# Compatible Cloud Images

The [Bintray website](https://bintray.com/vmware/photon/) contains the following cloud-ready images of Photon OS: 

1. GCE - Google Compute Engine

1. AMI - Amazon Machine Image

1. OVA

Because the cloud-ready images of Photon OS are built to be compatible with their corresponding cloud platform or format, you typically do not need to build a cloud image--just go to Bintray and download the image for the platform that you are working on. 

If, however, you want to build your own cloud image, perhaps because you seek to customize the code, see the next section on how to build cloud images.

## How to build cloud images

	sudo make cloud-image IMG_NAME=image-name

	image-name: gce/ami/azure/ova

The output of the build process produces the following file formats:

GCE - A tar file consisting of disk.raw as the raw disk file 

AMI - A raw disk file

<!-- Azure - A vhd file -->

OVA - An ova file (vmdk + ovf)

If you want, you can build all the cloud images by running the following command: 

	sudo make cloud-image-all 

<!-- ###How to build Photon bosh-stemcell

Please follow the link to [build](https://github.com/cloudfoundry/bosh/blob/develop/bosh-stemcell/README.md) Photon bosh-stemcell
-->

## How to create running instances in the cloud

The following sections contain some high-level instructions on how to create instances of Photon OS in the Google Compute Engine (GCE) and Amazon Elastic Cloud Compute (EC2). For more information, see the Amazon or Google cloud documentation. 

### GCE

The tar file can be uploaded to Google's cloud storage and an instance can be created after creating an image from the tar file. You will need the Google Cloud SDK on your host machine to upload the image and create instances.

####Install Google cloud SDK on host machine

	curl https://sdk.cloud.google.com | bash

####Upload the tar file

	gsutil cp photon-gce.tar.gz gs://bucket-name

####Create image

	gcloud compute --project project-id images create image-name --description description --source-uri https://storage.googleapis.com/bucket-name/photon-gce.tar.gz

####Create instance of GCE

	gcloud compute --project project-id instances create instance-name --zone "us-central1-f" --machine-type "n1-standard-1" other-options

(You can also create instances from the Google developer console.)

For more information, see [Running a Photon OS Machine on GCE](photon-admin-guide.md#running-a-photon-os-machine-on-gce). 

### AWS EC2

Install the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html#install-bundle-other-os) and [EC2 CLI](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html) tools. 

####Bundle the image

	ec2-bundle-image -c cert.pem -k private-key.pem -u $AWS_USER_ID --arch x86_64 --image photon-ami.raw --destination directory-name

####Upload the bundle

	ec2-upload-bundle --manifest directory-name/photon-ami.raw.manifest.xml --bucket bucket-name --access-key $AWS_ACCESS_KEY --secret-key $AWS_SECRET_KEY

####Register the AMI

	ec2-register bucket-name/photon-ami.raw.manifest.xml --name name --architecture x86_64 --virtualization-type hvm

You can now launch instances using the AWS console.

For more information, see [Customizing a Photon OS Machine on EC2](photon-admin-guide.md#customizing-a-photon-os-machine-on-ec2).


<!--
##AZURE

Install the [Azure CLI] (https://www.npmjs.com/package/azure)

Install [QEMU](https://en.wikibooks.org/wiki/QEMU/Installing_QEMU)

####Create the image
azure vm image create image_name path_to_vhd -l "West US" -o linux

Create running VM instances using Azure management portal
-->

###OVA

The OVA image uses an optimized version of the 4.4.8 Linux kernel. Two ova files are generated from the build: photon-ova.ova, which is the full version of Photon OS, and photon-custom.ova, which is the minimal version of Photon OS. The password for photon-ova.ova should be changed using guest customization options when you upload it to VMware vCenter. Photon-custom.ova comes with the default password set to `changeme`; you must change it the first time you log in.

#### OVA Prerequisites

[VDDK 6.0](https://developercenter.vmware.com/web/sdk/60/vddk)

To utilize the VDDK libraries the following procedure may be used, this extracts the libraries and temporarily exports them to the LD_LIBRARY_PATH for the *current session*.  (tested on Ubuntu 1404 & 1604)  If you wish to make this permenant and system-wide then you may want to create a config file in /etc/ld.so.conf.d/.

    tar -zxf VMware-vix-disklib-6.0.2-3566099.x86_64.tar.gz
    cp -r vmware-vix-disklib-distrib/include/* /usr/include/
    mkdir /usr/lib/vmware
    cp -a ~/vmware-vix-disklib-distrib/lib64/* /usr/lib/vmware/
    rm /usr/lib/vmware/libstdc++.so.6
    export LD_LIBRARY_PATH=/usr/lib/vmware

[OVFTOOL](https://my.vmware.com/group/vmware/details?downloadGroup=OVFTOOL410&productId=491)

OVF Tool should be downloaded and installed on the host.

    sh VMware-ovftool-4.1.0-2459827-lin.x86_64.bundle --eulas-agreed --required

<!-- 
##Photon Bosh

Please refer [bosh docs] (http://bosh.io/docs) to deploy BOSH on Photon 
-->



