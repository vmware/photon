## Prepare a workspace.

Pull the photon source code from github
```
git clone https://github.com/vmware/photon.git $HOME/workspaces/photon
```

Build the  docker container
```
docker build -t pdev $HOME/workspaces/photon/support/dockerfiles/ubuntu-dev
```

## Use the docker container
Run "make iso" inside the container
```
docker run -v $HOME/workspaces/photon:/workspace pdev make iso
```

## Interactive mode
Start the container in interactive mode
```
docker run -it -v $HOME/workspaces/photon:/workspace pdev
```
