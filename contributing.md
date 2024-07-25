# Contributing

The Photon OS project team welcomes contributions from the community.

If you wish to contribute code and you have not signed our Contributor License Agreement (CLA), our CLA-bot will take you through the process and update the issue when you open a [Pull Request](https://help.github.com/articles/creating-a-pull-request). If you have questions about the CLA process, see our CLA [FAQ](https://cla.vmware.com/faq) or contact us through the GitHub issue tracker.

This page presents guidelines for contributing to Photon OS. Following the guidelines helps to make the contribution process easy, collaborative, and productive.

## Submitting Bug Reports and Feature Requests

Please submit bug reports and feature requests by using our GitHub [Issues](https://github.com/vmware/photon/issues) page.

Before you submit a bug report about the code in the repository, please check the Issues page to see whether someone has already reported the problem. In the bug report, be as specific as possible about the error and the conditions under which it occurred. On what version and build did it occur? What are the steps to reproduce the bug?

Feature requests should fall within the scope of the project. Keep in mind that Photon OS is intended to be a minimalist Linux operating system geared toward hosting containerized applications and cloud-native applications.

## Pull Requests

Before submitting a pull request, please make sure that you can build Photon OS. See [Building an ISO from the Source Code for Photon OS](https://github.com/vmware/photon/blob/master/docs/photon_installation/build-photon.md).

## SPEC File Guidelines and Best Practices

### Upgrade

If you have specs with scripts in `%pre`, `%post`, `%preun`, or `%postun`, make sure that you have code that is in appropriate sections for upgrade and install.

%pre

    # First argument is 1 =&gt; New Installation
	# First argument is 2 =&gt; Upgrade
	case "$1" in
       1)
           echo 'new install'
          &nbsp;;;
       2)
           echo 'upgrade'
          &nbsp;;;
    esac

%post

	# First argument is 1 =&gt; New Installation
	# First argument is 2 =&gt; Upgrade
	case "$1" in
	   1)
	       echo 'new install'
	      &nbsp;;;
	   2)
	       echo 'upgrade'
	      &nbsp;;;
	esac

%preun

	# First argument is 0 =&gt; Uninstall
	# First argument is 1 =&gt; Upgrade
	case "$1" in
	   0)
	       echo 'new install'
	      &nbsp;;;
	   1)
	       echo 'upgrade'
	      &nbsp;;;
	esac

%postun

	# First argument is 0 =&gt; Uninstall
	# First argument is 1 =&gt; Upgrade
	case "$1" in
	   0)
	       echo 'new install'
	      &nbsp;;;
	   1)
	       echo 'upgrade'
	      &nbsp;;;
	esac

### Systemd Macros

To enable or deactivate a service in `post`, `preun`, `postun` sections, you can use the following macros.

	%post %systemd_post cloud-config.service //enables service

	%preun %systemd_preun cloud-final.service //deactivates service

	%postun %systemd_postun cloud-init.service //it does not do anything

Expansion of these macros:

	%systemd_post() \
	if [ $1 -eq 1 ]&nbsp;; then \
	        # Initial installation \
	        systemctl --no-reload preset&nbsp;%{?*} &gt;/dev/null 2&gt;&amp;1 ||&nbsp;: \
	fi \
	%{nil}

	%systemd_preun() \
	if [ $1 -eq 0 ]&nbsp;; then \
	        # Package removal, not upgrade \
	        systemctl --no-reload disable --now&nbsp;%{?*} &gt; /dev/null 2&gt;&amp;1 ||&nbsp;: \
	fi \
	%{nil}

	%systemd_postun()&nbsp;%{nil}

Note: The `systemd_postun` macro does not do anything. The `systemd_preun` macro deactivates the service, while `systemd_post` macro enables the service.


