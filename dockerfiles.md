# Photon on Docker

To create a Docker container image we need a Dockerfile that describes the base image and packages to be installed on the image. A Dockerfile lets you define and then create an image that can then be used to create container instances.
A Photon Dockerfile is located at following location:

```$HOME/workspace/photon/support/dockerfiles/photon```

## Build new Photon Images
To build new images you should have built all Photon RPMS using ```make all``` or ```make iso```. Also, the docker service should be running in the background.

The ```./make-docker-image.sh``` command takes the path of the local repo and the type of image (i.e. minimal, micro or full) you want to create.

```cd $HOME/workspace/photon/support/dockerfiles/photon```

```./make-docker-image.sh $HOME/workspace minimal```

## Running the Photon Container

```docker run -it photon:minimal```
