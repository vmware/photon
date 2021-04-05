+++
title = "Photon OS"
linkTitle = "VMware Photon OS Home"
+++
<!-- blocks/cover content start -->
{{< blocks/cover 
	title="Project Photon OS" 
	height="auto" 
	color="primary" 
	font_color="secondary" 
	subtitle="Photon OS is a Linux based, open source, security-hardened, enterprise grade appliance operating system that is purpose built for Cloud and Edge applications. ">}}

{{< cover-buttons 
	buttonTxt1="Learn More"
	buttonLink1="#features"

	buttonTxt2="Download"
	buttonLink2="https://github.com/vmware/photon/wiki/Downloading-Photon-OS"
	>}}

{{< /blocks/cover >}}
<!-- blocks/cover content end -->

<!-- blocks/homepage-grid start -->
{{< blocks/homepage-grid 

	textLead1="Virtual Machines and Bare Metal"
	textSub1="Run apps on bare metal, on hypervisors like VMware ESXi, or in the public cloud"
	gridImg1="vm-metal.svg"

	textLead2="Containers and Kubernetes" 
	textSub2="Use as a secure, stand-alone container host, or build cloud-scale Kubernetes nodes and clusters "
	gridImg2="multi-container-app.svg"

	textLead3="Local and Remote Development"
	textSub3="Use Photon OS as a Development Environment for building modern applications"
	gridImg3="dev-for-cloud.svg" >}}

<!-- blocks/homepage-grid End -->

<!-- blocks/downloads start -->
{{< blocks/downloads 
	textHead="Download Photon OS"
	textBigSub=`Download local images for x86, ARM64 and Raspberry Pi, or use Cloud images for environments like AWS, GCE, Azure, along with checksums and previous releases. `
	
	textLead1="ISO Images"
	textSub1=`Contains everything needed to install. Choose between a minimal or a full installation to suit your deployment needs. Photon can be <a href="docs/installation-guide/">installed from ISO directly</a>, or can be used with <a href="docs/user-guide/setting-up-network-pxe-boot/">PXE/kickstart environments for automated installations</a>`

	textLead2="OVA Appliance"
	textSub2=`Portable, ready-to-go virtual environment. <a href="https://github.com/vmware/photon/wiki/Downloading-Photon-OS">Photon OS Open Virtual Appliance packages</a> include a highly sanitized and optimized kernel and packages to streamline and standardize appliance deployments.`

	buttonURL="https://github.com/vmware/photon/wiki/Downloading-Photon-OS" 
	>}}
<!-- blocks/downloads end -->

<!-- blocks/use-cases begin -->
{{< blocks/use-cases 

	headline="Features"
	
	featuredImg2="security.svg"
	textLead2="Secure By Default"
	textSub2=`Using the recommendations of the <a href="https://www.kernel.org/doc/html/latest/security/self-protection.html" target="_blank">Kernel Self-Protection Project (KSPP)</a>, the Photon OS Linux Kernel is secure from the start. Packages are built with hardened security flags and can be easily updated and verified. `
	buttonTxt2="Read The Docs"
	buttonURL2="/docs/"
	
	featuredImg1="photon-container-host.svg"
	textLead1="Lightweight Container Host" 
	textSub1="Photon OS delivers just enough of a Linux operating system to efficiently run containers on VMware vSphere, Microsoft Azure, Google Compute Engine, and Amazon Elastic Compute Cloud"
	buttonTxt1="Read The Docs"
	buttonURL1="/docs/"

	featuredImg3="realtime-clock.svg"
	textLead3="Real Time Kernel Support"
	textSub3="Photon OS provides a performant stack for deployments like Virtual Radio Access Network applications that demand real time capabilities and ultra-low latency response"
	buttonTxt3="Read The Docs"
	buttonURL3="/docs/"
	>}}
<!-- blocks/use-cases end -->

<!-- blocks/contributing -->
{{% blocks/contributing
	
	textLead1="Contributing"
	
	textSub1=`The Photon project team welcomes contributions from the community. If you would like to contribute code and you have not signed our <a href="https://cla.vmware.com/faq" target="_blank">Contributor License Agreement (CLA)</a>, our CLA-bot will walk you through the process and update the issue when you open a Pull Request.`
	buttonTxt1="Fork Photon"
	buttonURL="https://github.com/vmware/photon"

	%}}
<!-- blocks/contributing end -->


<!-- blocks/team begin -->
{{< blocks/team  
	textHead="Team Photon"
	textSub=`Photon OS is released as open source software by an <a href="https://github.com/vmware/photon/graphs/contributors">epic team of contributors.</a>`
	>}}
<!-- blocks/team end -->



<!-- blocks/license start -->
{{< blocks/license 
	textLead1="License"
	textSub1=`The ISO and OVA images are distributed under the <a href="https://github.com/vmware/photon/blob/2.0/installer/EULA.txt" target="_blank">VMware Photon OS EULA.</a> Open source license information may be found the in Photon OS <a href="https://raw.githubusercontent.com/vmware/photon/master/COPYING" target="_blank">Open Source License</a> file.`


	textLead2="Support" 
	textSub2=`Photon OS is released as open source software and provides community support through our GitHub project page. If you encounter an issue or have a question, feel free to reach out on the  <a href="https://github.com/vmware/photon/issues" target="_blank">GitHub issues page for Photon OS</a>.`
	>}}
<!-- blocks/license end -->
<!-- blocks/getting-started begin -->
{{< blocks/getting-started 
	
	textLead1="Get Started"
	
	textSub1="See the documentation to get started with Photon OS"
	buttonTxt1="Documentation"
	buttonURL="/docs/"

	>}}
<!-- blocks/getting-started end -->