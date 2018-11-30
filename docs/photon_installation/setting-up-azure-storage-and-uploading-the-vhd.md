# Set Up Azure Storage and Uploading the VHD

You can use either the Azure Portal or the Azure CLI to set up your Azure storage space, upload the Photon OS VHD file, and create the Photon OS VM.

## Setting Up Using the Azure Portal

You can use the Azure portal to set up Photon OS 2.0 in the Azure cloud. The following instructions are brief. Refer to the Azure documentation for details.

1. Log in to the Azure portal at  [http://portal.azure.com](http://portal.azure.com/).
2. Create a resource group. In the toolbar, choose Resource Groups, click **+Add** , fill in the resource group fields, and choose **Create**.
3. Create a storage account. In the toolbar, choose Storage Accounts, click **+Add** , fill in the storage account fields (and the resource group you just created), and choose **Create**.
4. Select the storage account.
5. Scroll down the storage account control bar, click Containers (below BLOB SERVICE), click **+Container** , fill in the container fields, and choose **Create**.
6. Select the container you just created.
7. Click **Upload** and upload the Photon OS VHD image file to this container.
8. Once the VHD file is uploaded, refer to the Azure documentation for instructions on how to create and manage your Photon OS VM.

## Setting Up Using the Azure CLI

You can use the Azure CLI 2.0 to set up Photon OS. 

**Note:**  Except where overridden with parameter values, these commands create objects with default settings.

1. Create a resource group.

    From the Azure CLI, create a resource group.
    ````
    az group create \
     --name &lt;your_resource_group&gt; \
     --location westus
    ````

1. Create a storage account

    Create a storage account associated with this resource group.
    ````
    az storage account create \
        --resource-group &lt;your_resource_group&gt; \
        --location westus \
        --name &lt;your_account_name&gt; \
        --kind Storage \
        --sku Standard_LRS
    ````

1. List the Keys for the Storage Account

    Retrieve the keys associated with your newly created storage account.
    ````
    az storage account keys list \
        --resource-group &lt;your_resource_group&gt; \
        --account-name &lt;your_account_name&gt;
    ````
    
1. Create the Storage Container

    Create a storage container associated with your newly created storage account.
    
    **Note:** The sample create.sh script, described below, does this for you programmatically.
    ````
    az storage container create \
        --account-name &lt;your_account_name&gt; \
        --name &lt;your_container_name&gt;
    ````
1. Verify Your Setup in the Azure Portal

    1. Log into the Azure portal using your account credentials.
    2. From the left toolbar, click **Storage Accounts**. You should see your storage accounts.
    3. Select the storage account.
    4. Scroll down the storage account control bar and click **Containers** (below BLOB SERVICE). You should see the container you created.

1. Upload the Photon OS Distribution to Your Storage Container

    The Photon OS distribution for Azure is 16GB. You can download it locally or to a mounted, shared location.
    ````
    az storage blob upload \
        --account-name &lt;your_account_name&gt; \
        --account-key &lt;your_account_key&gt; \
        --container-name &lt;your_container_name&gt; \
        --type page \
        --file &lt;vhd_path&gt; \
        --name &lt;vm_name&gt;.vhd
    ````

### Example Setup Script

You can use the following script (create.sh) to upload your VHD file programmatically and create the VM. Before you run it, specify the following settings:

- resource_group name
- account_name
- account_key (public or private)
- container_name
- public_key_file
- vhd_path and and vm_name of the Photon OS VHD distribution file

The following script returns the complete IP address of the newly created VM.
````
#!/bin/bash
vhd_path=$1
vm_name=$2
export PATH=$PATH:/root/azure_new/bin/az
echo PATH=$PATH
resource_group=&quot;&quot;
account_name=&quot;&quot;
account_key=&quot;&quot;
container_name=&quot;mydisks&quot;
url=&quot;https://${account_name}.blob.core.windows.net/${container_name}/${vm_name}.vhd&quot;
public_key_file=&quot;/root/azure_new/jenkins.pub&quot;
echo &quot;########################&quot;
echo &quot;#   Create container   #&quot;
echo &quot;########################&quot;
/root/azure_new/bin/az storage container create --account-name ${account_name} --name ${container_name}
echo &quot;##################&quot;
echo &quot;#   Upload vhd   #&quot;
echo &quot;##################&quot;
/root/azure_new/bin/az storage blob upload --account-name ${account_name} \
    --account-key ${account_key} \
    --container-name ${container_name} \
    --type page \
    --file ${vhd_path} \
    --name ${vm_name}.vhd
echo &quot;##################&quot;
echo &quot;#   Create vm    #&quot;
echo &quot;##################&quot;
echo &quot;az vm create --resource-group ${resource_group} --location westus --name ${vm_name} --storage-account ${account_name} --os-type linux --admin-username michellew --ssh-key-value ${public_key_file} --image ${url} --use-unmanaged-disk ... ...&quot;
/root/azure_new/bin/az vm create --resource-group ${resource_group} --location westus --name ${vm_name} --storage-account ${account_name} --os-type linux --admin-username michellew --ssh-key-value ${public_key_file} --image ${url} --use-unmanaged-disk
````
