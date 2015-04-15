# == Class: vagrantbaseconfig
#
# Performs initial configuration tasks for all Vagrant boxes.
#
class vagrantbaseconfig {

  file {
    '/home/vagrant/.bashrc':
    owner  => 'vagrant',
    group  => 'vagrant',
    mode   => '0644',
    source => 'puppet:///modules/vagrantbaseconfig/bashrc.sh';
  }

  file {
    '/home/vagrant/.bash_profile':
    owner  => 'vagrant',
    group  => 'vagrant',
    mode   => '0644',
    source => 'puppet:///modules/vagrantbaseconfig/bash_profile.sh';
  }

  file {
    '/etc/sudoers':
    owner  => 'root',
    group  => 'root',
    mode   => '0440',
    source => 'puppet:///modules/vagrantbaseconfig/sudoers';
  }

  file {
    '/home/vagrant/.ssh':
    ensure => directory,
    owner  => 'vagrant',
    group  => 'vagrant',
    mode   => '0700',
  }

  file {
    '/home/vagrant/.ssh/authorized_keys':
    ensure  => present,
    owner   => 'vagrant',
    group   => 'vagrant',
    mode    => '0600',
    source  => 'puppet:///modules/vagrantbaseconfig/vagrant.pub',
    require => File['/home/vagrant/.ssh']
  }

  file {
    '/etc/ssh/sshd_config':
    path   => '/etc/ssh/sshd_config',
    owner  => root,
    group  => root,
    mode   => '0444',
    source => 'puppet:///modules/vagrantbaseconfig/sshd_config'
  }
}

