An official Vagrant box is available on Hashicorp Atlas. To get started: 

	vagrant init vmware/photon

Add the following lines to the Vagrantfile: 

	config.vm.provider "virtualbox" do |v|
	  v.customize ['modifyvm', :id, '--acpi', 'off']
	end

Install vagrant-guests-photon plugin which provides VMware Photon OS guest support.
It is available at https://github.com/vmware/vagrant-guests-photon.

Requires VirtualBox 4.3 or later version. If you have issues, please check your version.


