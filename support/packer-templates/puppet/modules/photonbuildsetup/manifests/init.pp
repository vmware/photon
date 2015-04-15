# == Class: photonbuildsetup
#
# Performs initial configuration tasks for all Vagrant boxes.
#
class photonbuildsetup {

  exec {
    'apt-get update':
      command => '/usr/bin/apt-get update',
  }

  package { ['build-essential',
            'gawk',
            'bison',
            'libgmp-dev',
            'libmpfr-dev',
            'libmpc-dev',
            'mkisofs',
            'cifs-utils',
            'createrepo',
            'rpm',
            'git',
            'htop',
            'python-aptdaemon',
            'gdisk',
            'texinfo']:
    ensure => present,
    require => Exec['apt-get update'];
  }

  file { '/bin/sh':
      ensure => 'link',
      target => '/bin/bash',
  }

  file {
    '/mnt/photonroot':
    ensure => directory,
    owner  => 'vagrant',
    group  => 'vagrant',
    mode   => '0755',
  }

}
