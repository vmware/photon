# Terminate the AMI Instance

Because Amazon charges you while the instance is running, you must shut it down when you have finsihed using it.  

1. Get the ID of the AMI so you can terminate it:
	
    ```
$ ec2-describe-instances
```

1. Terminate the Photon OS instance by running the following command: 
	
    ```
$ ec2-terminate-instances <instance-id>
```

    Replace the placeholder with the ID that the `ec2-describe-images` command returned. If you ran a second instance of Photon OS with the cloud-init file that runs docker, terminate that instance as well.