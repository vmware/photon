# Prerequisites

Before you use Photon OS with Amazon Elastic Cloud Compute, perform the following prerequisite tasks:

1. Verify that you have the following resources:
    
    - **AWS account**. Working with EC2 requires an Amazon account for AWS with valid payment information. Keep in mind that, if you try the examples in this document, you will be charged by Amazon. See [Setting Up with Amazon EC2](#http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html).
    - **Amazon tools**. The following examples also assume that you have installed and configured the Amazon AWS CLI and the EC2 CLI and AMI tools, including ec2-ami-tools.
    
    For more information, see [Installing the AWS Command Line Interface](#http://docs.aws.amazon.com/cli/latest/userguide/installing.html), [Setting Up the Amazon EC2 Command Line Interface Tools on Linux](#http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html), and [Configuring AWS Command-Line Interface](#http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). Also see [Setting Up the AMI Tools](#http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-up-ami-tools.html).
    
    The procedure in this section uses an Ubuntu 14.04 workstation to generate the keys and certificates that AWS requires.

1. Download the Photon OS image for Amazon. 

   VMware packages Photon OS as a cloud-ready Amazon machine image (AMI) that you can download for free from [Bintray](https://bintray.com/vmware/photon).

   Download the Photon OS AMI and save it on your workstation. For more infromation, see [Downloading Photon OS](Downloading-Photon-OS.md).

   **Note**: The AMI version of Photon is a virtual appliance with the information and packages that Amazon needs to launch an instance of Photon in the cloud. To build the AMI version, VMware starts with the minimal version of Photon OS and adds the sudo and tar packages to it. 