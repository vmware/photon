# Customizing a Photon OS Machine on EC2

You can upload an `ami` image of Photon OS to Amazon Elastic Compute Cloud (EC2) and customize the Photon OS machine by using `cloud-init` with an EC2 data source. The Amazon machine image version of Photon OS is available as a free download on Bintray at the location `https://bintray.com/vmware/photon/`.

The `cloud-init` service is commonly used on EC2 to configure the cloud instance of a Linux image. On EC2, `cloud-init` sets the `.ssh/authorized_keys` file to let you log in with a private key from another computer, that is, a computer besides the workstation that you are already using to connect with the Amazon cloud. 

## Example

The cloud-config user-data file that appears in the following example contains abridged SSH authorized keys to show you how to set them. 

### Prerequisites 

- To work with EC2, obtain Amazon accounts for both AWS and EC2 with valid payment information. If you execute the below examples, you will be charged by Amazon. You must replace the `<placeholders>` for access keys and other account information in the examples with your account information. 
- Install and set up the Amazon AWS CLI and the EC2 CLI tools, including `ec2-ami-tools`. 
    For more information, see [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html), [Setting Up the Amazon EC2 Command Line Interface Tools on Linux](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html) and [Setting Up the AMI Tools](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-up-ami-tools.html). 
- Create  SSH keys and an RSA user signing certificate and its corresponding private RSA key file.  

### Procedure 

1. Upload the Photon OS `.ami` image to the Amazon cloud and configure it with cloud-init. The correct virtualization type for Photon OS is `hvm`.   
	
    ```
$ mkdir bundled
	$ tar -zxvf ./photon-ami.tar.gz 
	$ ec2-bundle-image -c ec2-certificate.pem -k ec2-privatekey.pem -u <EC2 account id>  --arch x86_64 --image photon-ami.raw --destination ./bundled/
	$ aws s3 mb s3://<bucket-name>
	$ ec2-upload-bundle --manifest ./bundled/photon-ami.manifest.xml --bucket <bucket-name> --access-key <Account Access Key> --secret-key <Account Secret key>
	$ ec2-register <bucket-name>/photon-ami.manifest.xml --name photon-ami --architecture x86_64 --virtualization-type hvm
```

1. Import the cloud-config data. In the following command, the `--user-data-file` option instructs cloud-init to import the cloud-config data in `user-data.txt`. The command assumes you have uploaded the `user-data.txt file` and created the keypair `mykeypair` and the security group `photon-sg`.
   
    ```
 $ ec2-run-instances <ami-ID> --instance-type m3.medium -g photon-sg --key mykeypair --user-data-file user-data.txt
```
    Describe the instance to see its ID: 
	
    ```
$ ec2-describe-instances
```
    
1. Run the following command to obtain its public IP address, which you can use to connect to the instance with SSH:
	
    ```
$ aws ec2 describe-instances --instance-ids <instance-id> --query 'Reservations[*].Instances[*].PublicIpAddress' --output=text
	$ ec2-describe-images
```

1. Run the following commands to terminate the machine. It is important to shut down the machine because Amazon charges you while the host is running down.   

    ```
$ ec2-deregister <ami-image-identifier>
	$ ec2-terminate-instances <instance-id>
```

### Result

The following are the contents of the `user-data.txt` file that `cloud-init` applies to the machine the first time that it boots up in the cloud: 
    
```
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
	ssh_authorized_keys:
	 - ssh-rsa MIIEogIBAAKCAQEAuvHKAjBhpwuomcUTpIzJWRJAe71JyBgAWrwqyN1Mk5N+c9X5
	Ru2fazFA7WxQSD1KyTEvcuf8JzdBfrEJ0v3/nT2x63pvJ8fCl6HRkZtHo8zRu8vY
	KYTZS/sdvM/ruubHfq1ldRpgtYSqbkykoe6PCQIDAQABAoIBAEgveQtjVzHDhLTr
	rmwJmO316ERfkQ/chLaElhi9qwYJG/jqlNIISWFyztqD1b3fxU6m5MOBIujh7Xpg
	... ec3test@example.com
```

You can view the cloud-init output log file on EC2 at `/var/log/cloud-init-output.log`. 

For more information on using cloud-init user data on EC2, see [Running Commands on Your Linux Instance at Launch](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html).

For more information on how to get Photon OS up and running on EC2 and run a containerized application in the Docker engine, see [Running Photon OS on Amazon Elastic Cloud Compute](Running-Photon-OS-on-Amazon-Elastic-Cloud-Compute.md).

With Photon OS, you can also build cloud images on Google Compute Engine and other cloud providers. For more information, see [Compatible Cloud Images](cloud-images.md).