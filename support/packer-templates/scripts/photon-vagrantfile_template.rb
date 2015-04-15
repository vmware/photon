Vagrant.require_version '>= 1.6.2'

Vagrant.configure('2') do |config|

  config.vm.synced_folder '.', '/vagrant', disabled: true

  config.nfs.functional = false

  config.vm.network "forwarded_port", guest: 2375, host: 2375

  config.vm.provider :vmware_fusion do |v|
    v.gui = false
    v.vmx['ethernet0.virtualDev'] = 'vmxnet3'
  end

  config.vm.provider :vmware_workstation do |v|
    v.gui = false
    v.vmx['ethernet0.virtualDev'] = 'vmxnet3'
  end

  config.vm.provider :vcenter do |vcenter|
    vcenter.enable_vm_customization = false
  end
end
