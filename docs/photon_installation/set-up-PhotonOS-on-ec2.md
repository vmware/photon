# Set Up Photon OS on EC2

To run Photon OS on EC2, you must use cloud-init with an EC2 data source. The cloud-init service configures the cloud instance of a Linux image. An _instance_ is a virtual server in the Amazon cloud. 

The examples in this section show how to generate SSH and RSA keys for your Photon instance, upload the Photon OS `.ami` image to the Amazon cloud, and configure it with cloud-init. In the examples, replace information with your own paths, account details, or other information from Amazon. 

Perform the following steps to set up Photon OS on EC2

1. Create a key pair.

    Generate SSH keys on, for instance, an Ubuntu workstation: 
        	
    ```
    ssh-keygen -f ~/.ssh/mykeypair
    ```
    
    The command generates a public key in the file with a `.pub` extension and a private key in a file with no extension. Keep the private key file and remember the name of your key pair. The name is the file name of the two files without an extension. You will need the name later to connect to the Photon instance.
    
    Change the mode bits of the public key pair file to protect its security. In the command, include the path to the file if you need to.  
    	
    ```
    chown 600 mykeypair.pub
    ```
    
    Change the mode bits on your private key pair file so that only you can view it:  
    	
    ```
    chmod 400 mykeypair
    ```

    To import your public key pair file, but not your private key pair file, connect to the EC2 console at https://console.aws.amazon.com/ec2/ and select the region for the key pair. A key pair works only in one region, and the instance of Photon OS that will be uploaded later must be in the same region as the key pair. Select `key pairs` under `Network & Security`, and then import the public key pair file that you generated earlier. 
    
    For more information, see [Importing Your Own Key Pair to Amazon EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#how-to-generate-your-own-key-and-import-it-to-aws).

1. Generate a certificate.

    When you bundle up an image for EC2, Amazon requires an RSA user signing certificate. You create the certificate by using openssl to first generate a private RSA key and then to generate the RSA certificate that references the private RSA key. Amazon uses the pairing of the private key and the user signing certificate for  handshake verification. 
    
    1. On Ubuntu 14.04 or another workstation that includes `openssl`, run the following command to generate a private key. If you change the name of the key, keep in mind that you will need to include the name of the key in the next command, which generates the certificate.
       	
        ```
    openssl genrsa 2048 > myprivatersakey.pem
    ```
   
        Make a note of your private key as you will need it again later. 
    
    1. Run the following command to generate the certificate. The command prompts you to provide more information, but because you are generating a user signing certificate, not a server certificate, you can just type `Enter` for each prompt to leave all the fields blank.
    	
        ```
openssl req -new -x509 -nodes -sha256 -days 365 -key myprivatersakey.pem -outform PEM -out certificate.pem
```
   
        For more information, see the Create a Private Key and the Create the User Signing Certificate sections of [Setting Up the AMI Tools](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-up-ami-tools.html#ami-upload-bundle).
    
     1. Upload to AWS the certificate value from the `certificate.pem` file that you created in the previous command. Go to the Identity and Access Management console at https://console.aws.amazon.com/iam/, navigate to the name of your user, open the `Security Credentials` section, click `Manage Signing Certificates`, and then click `Upload Signing Certificate`. Open `certificate.pem` in a text editor, copy and paste the contents of the file into the `Certificate Body` field, and then click `Upload Signing Certificate`.
    
    For more information, see the Upload the User Signing Certificate section of [Setting Up the AMI Tools](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-up-ami-tools.html#ami-upload-bundle).

1. Create a security group.

    Create a security group and set it to allow SSH, HTTP, and HTTPS connections over ports 22, 80, and 443, respectively.
    Connect to the EC2 command-line interface and run the following commands: 
    
    	aws ec2 create-security-group --group-name photon-sg --description "My Photon security group"
    	{
    	    "GroupId": "sg-d027efb4"
    	}
    	aws ec2 authorize-security-group-ingress --group-name photon-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
    
    Make a note of the `GroupId` that is returned by EC2 as you will need it again later.
    
    By using `0.0.0.0/0` for SSH ingress on Port 22, you open the port to all IP addresses--which is not a security best practice but a convenience for the examples in this article. For a production instance or other instances that are anything more than temporary machines, you must authorize only a specific IP address or range of addresses. For more information, see [Authorizing Inbound Traffic for Linux Instances](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html).
    
    Repeat the command to allow incoming traffic on Port 80 and on Port 443: 
    
    	aws ec2 authorize-security-group-ingress --group-name photon-sg --protocol tcp --port 80 --cidr 0.0.0.0/0
    
    	aws ec2 authorize-security-group-ingress --group-name photon-sg --protocol tcp --port 443 --cidr 0.0.0.0/0
    
    Check your update: 
    
    	aws ec2 describe-security-groups --group-names photon-sg

1. Extract the tarball.

    Make a directory to store the image and then extract the Photon OS image from its archive by running the following `tar` command. If required, change the file name to match the version you have.    
    
    	mkdir bundled
    	tar -zxvf ./photon-ami.tar.gz

1. Bundle the image.

    Run the `ec2-bundle-image` command to create an instance store-backed Linux AMI from the Photon OS image that you extracted in the previous step. The result of the `ec2-bundle-image` command is a manifest that describes the machine in an XML file. 
    
    The command uses the certificate path to your PEM-encoded RSA public key certificate file, the path to your PEM-encoded RSA private key file, your EC2 user account ID; the correct architecture for Photon OS, the path to the Photon OS AMI image extracted from its tar file, and the `bundled` directory from the previous step. 
    
    Replace the values of the certificate path, the private key, and the user account with your own values.
    
    	$ ec2-bundle-image --cert certificate.pem --privatekey myprivatersakey.pem --user <EC2 account id>  --arch x86_64 --image photon-ami.raw --destination ./bundled/

1. Put the bundle in a bucket.

    Make an S3 bucket, replacing `<bucket-name>` with the name that you want. The command creates the bucket in the region specified in your Amazon configuration file, which should be the same region in which you are using your key pair file: 
    
    	$ aws s3 mb s3://<bucket-name>
    
    Upload the bundle to the Amazon S3 cloud. The following command includes the path to the XML file containing the manifest for the Photon OS machine created during the previous step, though you might have to change the file name to match the version you have. The manifest file is typically located in the same directory as the bundle. 
    
    The command also includes the name of the Amazon S3 bucket in which the bundle is to be stored; your AWS access key ID; and your AWS secret access key.
    
    	$ ec2-upload-bundle --manifest ./bundled/photon-ami.manifest.xml --bucket <bucket-name> --access-key <Account Access Key> --secret-key <Account Secret key>

1. Register the Image

    Run the following command to register the image. The command includes a name for the AMI, its architecture, and its virtualization type. The virtualization type for Photon OS is `hvm`.
    
    	$ ec2-register <bucket-name>/photon-ami.manifest.xml --name photon-ami --architecture x86_64 --virtualization-type hvm
    
    Once the image is registered, you can launch as many new instances as you require.

1. Run an instance of the image with Cloud-Init.

    In the below command, the `user-data-file` option instructs cloud-init to import the cloud-config data in `user-data.txt`.  
    
    Before you run the command, change directories to the directory containing the `mykeypair` file and add the path to the `user-data.txt`. 
    
    	$ ec2-run-instances <ami-ID> --instance-type m3.medium -g photon-sg --key mykeypair --user-data-file user-data.txt
    
    The command also includes the ID of the AMI, which you can obtain by running `ec2-describe-images`. Replace the instance type of `m3.medium` and the name of key pair with your own values to be able to connect to the instance. 
    
    The following are the contents of the `user-data.txt` file that `cloud-init` applies to the machine the first time it boots up in the cloud.  
    
    	#cloud-config
    	hostname: photon-on-01
    	groups:
    	- cloud-admins
    	- cloud-users
    	users:
    	- default
    	- name: photonadmin
    	   gecos: photon test admin user
    	   primary-group: cloud-admins
    	   groups: cloud-users
    	   lock-passwd: false
    	   passwd: vmware
    	- name: photonuser
    	   gecos: photon test user
    	   primary-group: cloud-users
    	   groups: users
    	   passwd: vmware
    	packages:
    	- vim

1. Get the IP address of your image.

    Run the following command to check on the state of the instance that you launched: 
    
    	$ ec2-describe-instances
    
    Obtain the external IP address of the instance by running the following query: 
    
    	$ aws ec2 describe-instances --instance-ids <instance-id> --query 'Reservations[*].Instances[*].PublicIpAddress' --output=text
    
Optionally, check the cloud-init output log file on EC2 at `/var/log/cloud-init-output.log` to see how EC2 handles the settings in the cloud-init data file. 
    
For more information on using cloud-init user data on EC2, see [Running Commands on Your Linux Instance at Launch](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html).