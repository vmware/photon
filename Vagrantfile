# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

# VM configuration, as we're compiling an OS from scratch, make sure the
# defaults are sensible.
vm_config = { ram: 2048, cpu: 2 }

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # the photon-build-machine box is built using packer,
  # see support/packer-templates/photon-build-machine.json
  config.vm.box = 'photon-build-machine'

  config.vm.box_check_update = false

  config.vm.provider('vmware_fusion') do |v|
    v.vmx['memsize'] = vm_config[:ram]
    v.vmx['numvcpus'] = vm_config[:cpu]
  end

  config.vm.provider('vmware_workstation') do |v|
    v.vmx['memsize'] = vm_config[:ram]
    v.vmx['numvcpus'] = vm_config[:cpu]
  end

  # Sync the current folder as /workspaces/photon using rsync.
  config.vm.synced_folder('.', '/workspaces/photon', type: 'rsync',
                          rsync__exclude: ['.git/', 'stage/']) # exclude .git and stage from sync.

  # Share the host's source root directory to copy back the build artifacts
  config.vm.synced_folder('.', '/workspaces/host_srcroot')

  # Build a new ISO and cleanup the machine afterward
  config.vm.provision('shell', path: 'support/vagrant/photon-build-machine-init.sh')
end
