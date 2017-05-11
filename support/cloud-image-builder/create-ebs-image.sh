#!/bin/bash

set -o errexit    # exit if any command returns non true return value
set -o nounset    # exit if you try to use uninitialised variable
set -x
PRGNAME=${0##*/}  # script name minus the path
LOGFILE="/var/log/${PRGNAME}-$(date +%Y-%m-%d).log"

#expected number of command line argument
NARGS=16
ARGS_PASSED=$#
VOLUME_SIZE=10
COPY_VOLUME_SIZE=20
DEVICE="/dev/xvdd"
COPY_DEVICE="/dev/xvdc"
EBS_IMAGE_ROOT_DEVICE_NAME="/dev/xvda"

while [[ $# > 0 ]]
do
        key="$1"
        shift

        case $key in
                -g|--GN)
                GROUP_NAME="$1"
                shift
        ;;
                -ai|--AMI_ID)
                AMI_ID="$1"
                shift
        ;;
                -tf|--TAR_FILE)
                TAR_FILE="$1"
                shift
        ;;
                -kn|--KEY_NAME)
                KEY_NAME="$1"
                shift
        ;;
                -n|--IMG_NAME)
                IMAGE_NAME="$1"
                shift
        ;;
                -aki|--ACCESS_KEY_ID)
                ACCESS_KEY_ID="$1"
                shift
        ;;
                -sak|--SECRET_ACCESS_KEY)
                SECRET_ACCESS_KEY="$1"
                shift
        ;;
                -dr|--DEFAULT_REGION)
                DEFAULT_REGION="$1"
                shift
        ;;
                -h|--help)
                echo 'Usage:'
                echo '-g|--GN                  :security group name for the instance'
                echo '-ai|--AMI_ID             :ami id for launching an instance'
                echo '-tf|--TAR_FILE           :tar filename without extension'
                echo '-kn|--KEY_NAME           :pem filename without pem extension to download'
                echo '-n|--IMG_NAME            :sets name of the ebs image'
                echo '-aki|--ACCESS_KEY_ID     :aws access key id'
                echo '-sak|--SECRET_ACCESS_KEY :aws secret access key'
                echo '-dr|--DEFAULT_REEGION    :aws default region'
                exit 0
        ;;
        *)
                # unknown option
        ;;
        esac
done

if [ $ARGS_PASSED -ne $NARGS ]; then
   echo "Error in the arguments passed. Try ./create-ebs-image.sh -h for help"
   exit 1
fi

#set the credential necessary to run the aws cli
export AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=$DEFAULT_REGION
KEY_FILE=$KEY_NAME.pem

#Start an AMI Instance
aws ec2 create-security-group --group-name $GROUP_NAME --description "AMI Creation Sec Group"
aws ec2 authorize-security-group-ingress --group-name $GROUP_NAME --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_FILE
chmod 400 $KEY_FILE
SECURITY_GROUP_ID=`aws ec2 describe-security-groups --group-name $GROUP_NAME --output=text --query 'SecurityGroups[0].GroupId'`
INSTANCE_ID=`aws ec2 run-instances --image-id $AMI_ID --security-group-ids $SECURITY_GROUP_ID --count 1 --instance-type m3.medium --key-name $KEY_NAME --output=text --query 'Instances[0].InstanceId'`
IP=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].PublicIpAddress'`
AVAILABILITY_ZONE=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].Placement.AvailabilityZone'`

while : ; do
 INSTANCE_STATE=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].State.Name'`
 if [ $INSTANCE_STATE == "running" ]; then
   break
 fi
done

sleep 30

ssh -o StrictHostKeyChecking=no -i $KEY_FILE root@$IP 'tdnf install -y kpartx wget'

#create two volumes one to copy the tar file and another for ebs image creation
VOLUMEID=`aws ec2 create-volume --size $VOLUME_SIZE --region $AWS_DEFAULT_REGION --availability-zone $AVAILABILITY_ZONE | grep VolumeId | cut -d"\"" -f4`
VOLUMEID_COPY=`aws ec2 create-volume --size $COPY_VOLUME_SIZE --region $AWS_DEFAULT_REGION --availability-zone $AVAILABILITY_ZONE | grep VolumeId | cut -d"\"" -f4`

#attach both the volumes
while : ; do
 STATE_1=`aws ec2 describe-volumes --volume-id $VOLUMEID_COPY --output text --query 'Volumes[0].State'`
 if [ $STATE_1 == "available" ]; then
   break
 fi
done

aws ec2 attach-volume --volume-id $VOLUMEID_COPY --instance-id $INSTANCE_ID --device $COPY_DEVICE --region $AWS_DEFAULT_REGION >> $LOGFILE

while : ; do
 STATE_2=`aws ec2 describe-volumes --volume-id $VOLUMEID_COPY --output text --query 'Volumes[0].Attachments[0].State'`
 if [ $STATE_2 == "attached" ]; then
   break
 fi
done

while : ; do
 STATE_3=`aws ec2 describe-volumes --volume-id $VOLUMEID --output text --query 'Volumes[0].State'`
 if [ $STATE_3 == "available" ]; then
   break
 fi
done

aws ec2 attach-volume --volume-id $VOLUMEID --instance-id $INSTANCE_ID --device $DEVICE --region $AWS_DEFAULT_REGION >> $LOGFILE

while : ; do
 STATE_4=`aws ec2 describe-volumes --volume-id $VOLUMEID  --output text --query 'Volumes[0].Attachments[0].State'`
 if [ $STATE_4 == "attached" ]; then
   break
 fi
done

#Copy the image file
ssh -i $KEY_FILE root@$IP 'rm -rf /mnt/copy; rm -rf /mnt/ebs; mkdir /mnt/copy; mkdir /mnt/ebs' >> $LOGFILE
ssh -i $KEY_FILE root@$IP "mkfs.ext4 $COPY_DEVICE" >> $LOGFILE
ssh -i $KEY_FILE root@$IP "mount $COPY_DEVICE /mnt/copy" >> $LOGFILE
scp -i $KEY_FILE $TAR_FILE.tar.gz root@$IP:/mnt/copy >> $LOGFILE
ssh -i $KEY_FILE root@$IP "cd /mnt/copy; tar -xf $TAR_FILE.tar.gz; dd if=$TAR_FILE.raw of=$DEVICE bs=1M" >> $LOGFILE
ssh -i $KEY_FILE root@$IP 'umount /mnt/copy'
ssh -i $KEY_FILE root@$IP 'rm -rf /mnt/copy /mnt/ebs'

#detach the volume
aws ec2 detach-volume --volume-id $VOLUMEID --region $AWS_DEFAULT_REGION >> $LOGFILE
aws ec2 detach-volume --volume-id $VOLUMEID_COPY --region $AWS_DEFAULT_REGION >> $LOGFILE

#create the snapshot
SNAPSHOT_ID=`aws ec2 create-snapshot --region $AWS_DEFAULT_REGION --description "photonOS ebs ami" --volume-id $VOLUMEID  | grep SnapshotId | cut -d"\"" -f4`
echo $SNAPSHOT_ID

#wait for the snapshot creation to succeed. This takes some time
while : ; do
 PROGRESS=`aws ec2 describe-snapshots --region $AWS_DEFAULT_REGION --snapshot-id $SNAPSHOT_ID | grep Progress | cut -d"\"" -f4`
 echo $PROGRESS
 if [ $PROGRESS == "100%" ]; then
   break
 fi
 sleep 60
done

#register the image name
aws ec2 register-image --region $AWS_DEFAULT_REGION --name $IMAGE_NAME --root-device-name $EBS_IMAGE_ROOT_DEVICE_NAME --block-device-mappings DeviceName=$EBS_IMAGE_ROOT_DEVICE_NAME,Ebs={SnapshotId=$SNAPSHOT_ID} --virtualization-type hvm --architecture x86_64
