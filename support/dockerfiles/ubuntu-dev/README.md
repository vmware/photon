## Prepare a workspace.

Pull the photon source code from github

```shell
git clone https://github.com/vmware/photon.git $HOME/workspaces/photon
```

Build the  docker container

```shell
docker build -t pdev $HOME/workspaces/photon/support/dockerfiles/ubuntu-dev
```

## Use the docker container
Run "make iso" inside the container

```shell
docker run --privileged -v $HOME/workspaces/photon:/workspace pdev make iso
```

## Interactive mode
Start the container in interactive mode

```shell
docker run --privileged -it -v $HOME/workspaces/photon:/workspace pdev
```
