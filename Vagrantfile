# -*- mode: ruby -*-
# vi: set ft=ruby :

module OS
  def OS.windows?
    (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
  end

  def OS.mac?
   (/darwin/ =~ RUBY_PLATFORM) != nil
  end

  def OS.unix?
    !OS.windows?
  end

  def OS.linux?
    OS.unix? and not OS.mac?
  end
end

ENV['VAGRANT_DEFAULT_PROVIDER'] ||= OS.mac? ? 'vmware_fusion' : "vmware_workstation"

fusion_path="/Applications/VMware Fusion.app/Contents/Library"
if File.directory?(fusion_path)
  ENV['PATH'] = "#{fusion_path}:#{ENV['PATH']}"
end

appcatalyst_path="/opt/vmware/appcatalyst/libexec"
if File.directory?(appcatalyst_path)
  ENV['PATH'] = "#{appcatalyst_path}:#{ENV['PATH']}"
end

# Hey Now! thanks StackOverflow: http://stackoverflow.com/a/28801317/1233435
req_plugins = %w(vagrant-triggers)

if OS.mac?
  req_plugins << "vagrant-vmware-fusion" if File.directory?(fusion_path)
  req_plugins << "vagrant-vmware-appcatalyst" if File.directory?(appcatalyst_path)
else
  req_plugins << "vagrant-vmware-workstation"
end

# Cycle through the required plugins and install what's missing.
plugins_install = req_plugins.select { |plugin| !Vagrant.has_plugin? plugin }
licensed_plugins = plugins_install.select { |plugin| plugin =~ /vagrant-vmware-(?:fusion|workstation)$/ }
licensed_plugins.each do |plugin|
  unless File.exist? "#{ENV["VAGRANT_VMWARE_LICENSE_FILE"]||"./#{plugin}.lic"}"
    abort "Failed to configure license, you can configure the path with VAGRANT_VMWARE_LICENSE_FILE"
  end
end

unless plugins_install.empty?
  puts "Installing plugins: #{plugins_install.join(' ')}"
  if system "vagrant plugin install #{plugins_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort 'Installation of one or more plugins has failed. Aborting.'
  end
end

licensed_plugins.each do |plugin|
  unless system "vagrant plugin license #{plugin} #{ENV["VAGRANT_VMWARE_LICENSE_FILE"]||"./#{plugin}.lic"}"
    abort "Failed to configure license, you can configure the path with VAGRANT_VMWARE_LICENSE_FILE"
  end
end

VAGRANTFILE_API_VERSION = '2'

# VM configuration, as we're compiling an OS from scratch, make sure the
# defaults are sensible.
vm_config = { ram: 2048, cpu: 2 }

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # the photon-build-machine box is built using packer,
  # see support/packer-templates/photon-build-machine.json
  config.vm.box = 'vmware/photon-build-machine'

  config.vm.box_check_update = false

  %w(vmware_fusion vmware_workstation vmware_appcatalyst).each do |p|
    config.vm.provider p do |v|
      v.vmx['memsize'] = vm_config[:ram]
      v.vmx['numvcpus'] = vm_config[:cpu]
      v.vmx['ethernet0.virtualDev'] = 'vmxnet3'
      v.vmx['vhv.enable'] = 'true'
    end
  end

  # Sync the current folder as /workspaces/photon using rsync.
  config.vm.synced_folder('.', '/workspaces/photon', type: 'rsync',
                          rsync__exclude: ['.git/', 'stage/']) # exclude .git and stage from sync.

  # Share the host's source root directory to copy back the build artifacts
  config.vm.synced_folder('.', '/workspaces/host_srcroot')

  # Build a new ISO and cleanup the machine afterward
  config.vm.provision('shell', path: 'support/vagrant/photon-build-machine-init.sh')
end
