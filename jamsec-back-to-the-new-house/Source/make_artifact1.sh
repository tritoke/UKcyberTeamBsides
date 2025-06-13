#!/bin/bash
# VM image creator @R&D-SANS

help()
{
    echo "This script creates snapshots for STI Images Only"
    echo "Usage: "
    echo "Parameters:"
    echo "- r: VM resource Group"
    echo "- v: VM Name"
    echo "- h: help"
}



touch /tmp/STI-snapper.log


TMP=/tmp/STI-snapper.json
LOG=/tmp/STI-snapper.log

#Environment Variables
export AZURE_STORAGE_KEY={xxxxx}
export AZURE_STORAGE_ACCOUNT=xxxxx
export SUBSCRIPTION_ID=xxxxxx
export CONTAINER_ID=sti-snapshots
# Arguments
while getopts :r:v:h: optname; do

  case $optname in
    r) #Resource Group Name
      RESOURCE_GROUP=${OPTARG}
      ;;
    v) #VM Name
      VM_NAME=${OPTARG}
      ;;
    h) #Show help
      help
      exit 2
      ;;
    \?) #Unrecognized option - show help
      echo -e \\n"Option -${BOLD}$OPTARG${NORM} not allowed."
      help
      exit 2
      ;;
  esac
done
az snapshot revoke-access --name "snap_$VM_NAME" --resource-group $RESOURCE_GROUP
az snapshot delete --name "snap_$VM_NAME" --resource-group $RESOURCE_GROUP
DISK=`az vm show -g $RESOURCE_GROUP -n $VM_NAME --query storageProfile.osDisk.name | tr -d \"`
echo "found disk ID: $DISK" >> $LOG
echo "Disk ids: $DISK"
SNAPSHOT=`az snapshot create -g $RESOURCE_GROUP -n snap_$VM_NAME --source $DISK --for-upload --query id | tr -d \"`
echo "Created Snapshot with ID: $SNAPSHOT" >> $LOG
echo "Creating SnapShot, Please wait..."
#sleep 50
#echo `az snapshot show --ids $SNAPSHOT` >> $LOG
STATE=`az snapshot show --ids $SNAPSHOT --query provisioningState | tr -d \"`
if [[ $STATE != "Succeeded" ]]
    then
        sleep 10
        echo "Waiting for Snapshot"
fi

SAS=`az snapshot grant-access --duration-in-seconds 3600 --ids $SNAPSHOT --query accessSas | tr -d \"`
echo "SAS key created"
echo "$SAS"
echo "$CONTAINER_ID"
echo "$VM_NAME"
echo "$STATE"
echo "$SNAPSHOT"
echo "Starting Copy operation"
az storage blob copy start --account-key $AZURE_STORAGE_KEY --account-name $AZURE_STORAGE_ACCOUNT --destination-container $CONTAINER_ID --destination-blob $VM_NAME.vhd --source-uri "$SAS"
