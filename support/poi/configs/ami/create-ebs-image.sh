#!/bin/bash

set -o errexit    # exit if any command returns non true return value
set -o nounset    # exit if you try to use uninitialised variable
set -x
PRGNAME=${0##*/}  # script name minus the path
LOGFILE="${PRGNAME}-$(date +%Y-%m-%d).log"

#expected number of command line argument
NARGS=16
ARGS_PASSED=$#
VOLUME_SIZE=10
COPY_VOLUME_SIZE=20
DEVICE="/dev/xvdd"
COPY_DEVICE="/dev/xvdc"
EBS_IMAGE_ROOT_DEVICE_NAME="/dev/xvda"
LOOP_WAIT=2
SSH_WAIT=30
SNAPSHOT_WAIT=60
LOOP_TRIAL=100

#AMI_IDS of different US Regions
AMI_ID_US_EAST_1="ami-83614695"
AMI_ID_US_EAST_2="ami-45311120"
AMI_ID_US_WEST_1="ami-e04b6380"
AMI_ID_US_WEST_2="ami-c0df50a0"

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
                echo '-ai|--AMI_ID             :ami id for launching an instance. This is optional'
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

if [ $ARGS_PASSED -eq $[$NARGS-2] ]; then
  if [ ! -z "${AMI_ID:-}" ]; then
   echo "Error in the arguments passed. Try ./create-ebs-image.sh -h for help"
   exit 1
  fi
  key=$DEFAULT_REGION
  case $key in
      us-east-1)
      AMI_ID=$AMI_ID_US_EAST_1
  ;;
      us-east-2)
      AMI_ID=$AMI_ID_US_EAST_2
  ;;
      us-west-1)
      AMI_ID=$AMI_ID_US_WEST_1
  ;;
      us-west-2)
      AMI_ID=$AMI_ID_US_WEST_2
  ;;
  *)
      #unkown region
      exit 1
  esac
  ARGS_PASSED=$[$ARGS_PASSED+2]
fi

if [ $ARGS_PASSED -ne $NARGS ]; then
   echo "Error in the arguments passed. Try ./create-ebs-image.sh -h for help"
   exit 1
fi

#set the credential necessary to run the aws cli
export AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=$DEFAULT_REGION
KEY_FILE=$KEY_NAME.pem

function cleanup {
  if [ ! -z "${INSTANCE_ID:-}" ]; then
   aws ec2 terminate-instances --instance-ids $INSTANCE_ID
   while : ; do
    INSTANCE_STATE=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].State.Name'`
    if [ "$INSTANCE_STATE" == "terminated" ]; then
      break
    fi
    sleep $LOOP_WAIT
   done
  fi
  if [ ! -z "${VOLUMEID_COPY:-}" ]; then
   aws ec2 delete-volume --volume-id $VOLUMEID_COPY
  fi
  if [ ! -z "${GROUP_NAME:-}" ]; then
   aws ec2 delete-security-group --group-name $GROUP_NAME
  fi
  if [ ! -z "${KEY_NAME:-}" ]; then
   aws ec2 delete-key-pair --key-name $KEY_NAME
  fi
  rm $KEY_FILE
}
trap 'cleanup' EXIT

function check_counter {
   if [ $# -ne 3 ]; then
      echo "Pass the counter,max value and the error message"
      exit 1
   fi
   if [ $1 -ge $2 ]; then
      echo "$3" >> $LOGFILE
      exit
   fi
}

#Start an AMI Instance
aws ec2 create-security-group --group-name $GROUP_NAME --description "AMI Creation Sec Group"
aws ec2 authorize-security-group-ingress --group-name $GROUP_NAME --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_FILE
chmod 400 $KEY_FILE
SECURITY_GROUP_ID=`aws ec2 describe-security-groups --group-name $GROUP_NAME --output=text --query 'SecurityGroups[0].GroupId'`
INSTANCE_ID=`aws ec2 run-instances --image-id $AMI_ID --security-group-ids $SECURITY_GROUP_ID --count 1 --instance-type m3.medium --key-name $KEY_NAME --output=text --query 'Instances[0].InstanceId'`
AVAILABILITY_ZONE=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].Placement.AvailabilityZone'`

count=0
while : ; do
 INSTANCE_STATE=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].State.Name'`
 if [ "$INSTANCE_STATE" == "running" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Instance $INSTANCE_ID not in running state" 
 sleep $LOOP_WAIT
done

count=0
while : ; do
 IP=`aws ec2 describe-instances --instance-ids $INSTANCE_ID --output=text --query 'Reservations[0].Instances[0].PublicIpAddress'`
 if [ "$IP" == "None" ]; then
   count=$[$count+1]
 else
   break
 fi
 check_counter $count $LOOP_TRIAL "Instance $INSTANCE_ID does not have an IP yet" 
 sleep $LOOP_WAIT
done

sleep $SSH_WAIT

while : ; do
 output=$(eval ssh -o StrictHostKeyChecking=no -i $KEY_FILE root@$IP 'tdnf install -y kpartx wget')
 ret=$?
 if [ "$ret" -eq 0 ]; then
  break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Unable to ssh the Instance $INSTANCE_ID with IP $IP" 
 sleep $LOOP_WAIT
done

#create two volumes one to copy the tar file and another for ebs image creation
VOLUMEID=`aws ec2 create-volume --size $VOLUME_SIZE --region $AWS_DEFAULT_REGION --availability-zone $AVAILABILITY_ZONE --output=text --query 'VolumeId'`
VOLUMEID_COPY=`aws ec2 create-volume --size $COPY_VOLUME_SIZE --region $AWS_DEFAULT_REGION --availability-zone $AVAILABILITY_ZONE --output=text --query 'VolumeId'`

#attach both the volumes
count=0
while : ; do
 STATE_1=`aws ec2 describe-volumes --volume-id $VOLUMEID_COPY --output=text --query 'Volumes[0].State'`
 if [ "$STATE_1" == "available" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Volume with ID $VOLUMEID_COPY is not available"
 sleep $LOOP_WAIT
done

aws ec2 attach-volume --volume-id $VOLUMEID_COPY --instance-id $INSTANCE_ID --device $COPY_DEVICE --region $AWS_DEFAULT_REGION >> $LOGFILE

count=0
while : ; do
 STATE_2=`aws ec2 describe-volumes --volume-id $VOLUMEID_COPY --output=text --query 'Volumes[0].Attachments[0].State'`
 if [ "$STATE_2" == "attached" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Volume with ID $VOLUMEID_COPY is not in attached state"
 sleep $LOOP_WAIT
done

count=0
while : ; do
 STATE_3=`aws ec2 describe-volumes --volume-id $VOLUMEID --output=text --query 'Volumes[0].State'`
 if [ "$STATE_3" == "available" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Volume with ID $VOLUMEID is not available"
 sleep $LOOP_WAIT
done

aws ec2 attach-volume --volume-id $VOLUMEID --instance-id $INSTANCE_ID --device $DEVICE --region $AWS_DEFAULT_REGION >> $LOGFILE

count=0
while : ; do
 STATE_4=`aws ec2 describe-volumes --volume-id $VOLUMEID  --output text --query 'Volumes[0].Attachments[0].State'`
 if [ "$STATE_4" == "attached" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Volume with ID $VOLUMEID is not in attached state"
 sleep $LOOP_WAIT
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

#wait for the volume to detach
count=0
while : ; do
 STATE_5=`aws ec2 describe-volumes --volume-id $VOLUMEID  --output text --query 'Volumes[0].Attachments[0].State'`
 if [ "$STATE_5" == "detached" ] || [ "$STATE_5" == "None" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Volume with ID $VOLUMEID is not in detached state"
 sleep $LOOP_WAIT
done

#create the snapshot
SNAPSHOT_ID=`aws ec2 create-snapshot --region $AWS_DEFAULT_REGION --description $TAR_FILE --volume-id $VOLUMEID --output=text --query 'SnapshotId'`

#wait for the snapshot creation to succeed. This takes some time
count=0
while : ; do
 PROGRESS=`aws ec2 describe-snapshots --region $AWS_DEFAULT_REGION --snapshot-id $SNAPSHOT_ID --output=text --query 'Snapshots[0].Progress'`
 echo $PROGRESS
 if [ "$PROGRESS" == "100%" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Snapshot creation for snapshot with ID $SNAPSHOT_ID failed"
 sleep $SNAPSHOT_WAIT
done

#register the image name
AMI_IMAGE_ID=`aws ec2 register-image --region $AWS_DEFAULT_REGION --name $TAR_FILE --root-device-name $EBS_IMAGE_ROOT_DEVICE_NAME --sriov-net-support simple --ena-support --block-device-mappings DeviceName=$EBS_IMAGE_ROOT_DEVICE_NAME,Ebs={SnapshotId=$SNAPSHOT_ID} --virtualization-type hvm --architecture x86_64 --output=text --query 'ImageId'`

#check the status of the AMI
count=0
while : ; do
 AMI_STATE=`aws ec2 describe-images --image-ids $AMI_IMAGE_ID --output=text --query 'Images[0].State'`
 echo $AMI_STATE
 if [ "$AMI_STATE" == "available" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Registering AMI with AMI ID $AMI_IMAGE_ID and $SNAPSHOT_ID failed"
 sleep $SNAPSHOT_WAIT
done

#Make AMI Public
aws ec2 modify-image-attribute --image-id $AMI_IMAGE_ID --launch-permission "{\"Add\":[{\"Group\":\"all\"}]}"

#Loop till AMI is public
count=0
while : ; do
 PUBLIC=`aws ec2 describe-images --image-ids $AMI_IMAGE_ID --output=text --query 'Images[0].Public'`
 echo $PUBLIC
 if [ "$PUBLIC" == "True" ]; then
   break
 else
  count=$[$count+1]
 fi
 check_counter $count $LOOP_TRIAL "Making the AMI with AMI ID $AMI_IMAGE_ID Public failed"
 sleep $LOOP_WAIT
done

aws ec2 create-tags --resources $SNAPSHOT_ID --tags Key=Name,Value=$IMAGE_NAME
aws ec2 create-tags --resources $AMI_IMAGE_ID --tags Key=Name,Value=$IMAGE_NAME

echo "SUCCESS: AMI with ID $AMI_IMAGE_ID was registered and made Public"
