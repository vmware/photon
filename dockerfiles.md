# Photon on Docker

To create Docker container image we need a Dockerfile that contains the filesystem and packages to be instaled on the images. Dockerfile lets create an image and then images are used to create container instances. 
Photon Dockerfile is located at following location.
 *  $HOME/workspace/photon/support/dockerfiles/photon

## Build new Photon Images
To build new images you should have built all photon RPMS using 'make all' or 'make iso'. Also docker service should be running in the background.

./make-docker-image.sh takes the path of the local repo and the type of image (i.e. minima, micro or full) you want to create.

 *  cd $HOME/workspace/photon/support/dockerfiles/photon
 *  ./make-docker-image.sh $HOME/workspace minimal
 
## Running Photon Container
 
 *  docker run -it photon:minimal
  


 
