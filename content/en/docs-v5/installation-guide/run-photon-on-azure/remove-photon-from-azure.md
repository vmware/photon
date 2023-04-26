---
title:  Remove Photon OS From Azure
weight: 3
---

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
resource_group=""
account_name=""
account_key=""
container_name="mydisks"
url="https://${account_name}.blob.core.windows.net/${container_name}/${vm_name}.vhd"
public_key_file="/root/azure_new/jenkins.pub"
exit_code=0
echo "##################"
echo "#   Delete vm    #"
echo "##################"
echo "az vm list  --resource-group ${resource_group} ... ..."
/root/azure_new/bin/az vm list  --resource-group ${resource_group}
echo "az vm delete --resource-group ${resource_group} --name ${vm_name} --yes ... ..."
/root/azure_new/bin/az vm delete --resource-group ${resource_group} --name ${vm_name} --yes
if [$? -ne 0];then
   exit_code=1
fi
echo "az vm list  --resource-group ${resource_group} ... ..."
/root/azure_new/bin/az vm list  --resource-group ${resource_group}
echo "##############$####"
echo "#   Delete vhd    #"
echo "###############$###"
echo "az storage blob list --account-name ${account_name} --container-name ${container_name} ... ..."
/root/azure_new/bin/az storage blob list --account-name ${account_name} --container-name ${container_name}
echo "az storage blob delete --account-name ${account_name} --container-name ${container_name} --name ${vm_name}.vhd ... ..."
/root/azure_new/bin/az storage blob delete --account-name ${account_name} --container-name ${container_name} --name ${vm_name}.vhd
if [$? -ne 0];then
   exit_code=1
fi
echo "az storage blob list --account-name ${account_name} --container-name ${container_name} ... ..."
/root/azure_new/bin/az storage blob list --account-name ${account_name} --container-name ${container_name}
echo "########################"
echo "#   Delete container   #"
echo "########################"
/root/azure_new/bin/az storage container delete --account-name ${account_name} --name ${container_name}
/root/azure_new/bin/az storage container delete --account-name ${account_name} --name vhds
exit ${exit_code}
````

You can now proceed to [Deploying a Containerized Application in Photon OS](../../deploying-a-containerized-application-in-photon-os/).