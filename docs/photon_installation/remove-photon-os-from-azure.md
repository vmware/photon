# Remove Photon OS From Azure

You can use the following delete.sh script to programmatically and silently remove the VM instance, VHD file, and container.

Consider deleting idle VMs so that you are not charged when not in use.

Before you run it, specify the following settings:

- resource_group name (from step 1, above)
- account_name (from step 2, above)
- account_key (public or private) (from step 3, above)
- container_name (from step 4, above)
- public_key_file
- vm_name of the Photon OS VHD distribution file

**delete.sh**

````
#!/bin/bash
vm_name=$1
resource_group=&quot;&quot;
account_name=&quot;&quot;
account_key=&quot;&quot;
container_name=&quot;mydisks&quot;
url=&quot;https://${account_name}.blob.core.windows.net/${container_name}/${vm_name}.vhd&quot;
public_key_file=&quot;/root/azure_new/jenkins.pub&quot;
exit_code=0
echo &quot;##################&quot;
echo &quot;#   Delete vm    #&quot;
echo &quot;##################&quot;
echo &quot;az vm list  --resource-group ${resource_group} ... ...&quot;
/root/azure_new/bin/az vm list  --resource-group ${resource_group}
echo &quot;az vm delete --resource-group ${resource_group} --name ${vm_name} --yes ... ...&quot;
/root/azure_new/bin/az vm delete --resource-group ${resource_group} --name ${vm_name} --yes
if [$? -ne 0];then
   exit_code=1
fi
echo &quot;az vm list  --resource-group ${resource_group} ... ...&quot;
/root/azure_new/bin/az vm list  --resource-group ${resource_group}
echo &quot;##############$####&quot;
echo &quot;#   Delete vhd    #&quot;
echo &quot;###############$###&quot;
echo &quot;az storage blob list --account-name ${account_name} --container-name ${container_name} ... ...&quot;
/root/azure_new/bin/az storage blob list --account-name ${account_name} --container-name ${container_name}
echo &quot;az storage blob delete --account-name ${account_name} --container-name ${container_name} --name ${vm_name}.vhd ... ...&quot;
/root/azure_new/bin/az storage blob delete --account-name ${account_name} --container-name ${container_name} --name ${vm_name}.vhd
if [$? -ne 0];then
   exit_code=1
fi
echo &quot;az storage blob list --account-name ${account_name} --container-name ${container_name} ... ...&quot;
/root/azure_new/bin/az storage blob list --account-name ${account_name} --container-name ${container_name}
echo &quot;########################&quot;
echo &quot;#   Delete container   #&quot;
echo &quot;########################&quot;
/root/azure_new/bin/az storage container delete --account-name ${account_name} --name ${container_name}
/root/azure_new/bin/az storage container delete --account-name ${account_name} --name vhds
exit ${exit_code}
````

You can now proceed to [Deploying a Containerized Application in Photon OS](deploying-a-containerized-application-in-photon-os.md).