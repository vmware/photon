#Supported Cloud Images

GCE - Google Compute Engine
AMI - Amazon Machine Image
Azure
OVA

How to build cloud images

sudo make cloud-image IMG_NAME=image-name

image-name : gce/ami/azure/ova

The output of the build process produces the following file formats:

GCE - A tar file consisting of disk.raw as the raw disk file 

AMI - A raw disk file

Azure - A vhd file

OVA - An ova file (vmdk + ovf)

sudo make cloud-image-all builds all the cloud images


#How to create running instances in the cloud


##GCE

The tar file can be uploaded to Google's cloud storage and an instance can be created after creating an image from the tar file. You will need Google Cloud sdk on host machine to upload the image and create instances

####Install google cloud sdk on host machine
curl https://sdk.cloud.google.com | bash

####Upload the tar file
gsutil cp photon-gce.tar.gz gs://bucket-name

####Create image
gcloud compute --project project-id images create image-name --description description --source-uri https://storage.googleapis.com/bucket-name/photon-gce.tar.gz

####Create instance of GCE
gcloud compute --project project-id instances create instance-name --zone "us-central1-f" --machine-type "n1-standard-1" other-options

You can create instances also from Google developer console


##AMI

Install the [AWS CLI] (http://docs.aws.amazon.com/cli/latest/userguide/installing.html#install-bundle-other-os)

####Bundle the image
ec2-bundle-image -c cert.pem -k private-key.pem -u $AWS_USER_ID --arch x86_64 --image photon-ami.raw --destination directory-name

####Upload the bundle
ec2-upload-bundle --manifest directory-name/photon-ami.raw.manifest.xml --bucket bucket-name --access-key $AWS_ACCESS_KEY --secret-key $AWS_SECRET_KEY
####Register the AMI
ec2-register bucket-name/photon-ami.raw.manifest.xml --name name --architecture x86_64 --virtualization-type hvm

You can now launch instances using AWS console


##AZURE

Install the [Azure CLI] (https://www.npmjs.com/package/azure)

Install [QEMU](https://en.wikibooks.org/wiki/QEMU/Installing_QEMU)

####Create the image
azure vm image create image_name path_to_vhd -l "West US" -o linux

Create running VM instances using Azure management portal


##OVA

The ova image uses a custom linux kernel, which is an optimized kernel based on version 4.1.3. Two ova files are generated from build - photon-ova.ova and photon-custom.ova. The password for photon-ova.ova should be changed using guest customization options when uploading to vCA. Photon-custom.ova is genrated with the password changeme, intended for use with Fusion/Workstation.

####Pre-requisites

[VDDK 6.0] (https://developercenter.vmware.com/web/sdk/60/vddk)

	- You must copy the libraries to /usr/lib/vmware and run ldconfig

	- Also copy the include files to /usr/include

[OVFTOOL] (https://my.vmware.com/group/vmware/details?downloadGroup=OVFTOOL410&productId=491)


