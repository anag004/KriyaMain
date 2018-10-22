#!/bin/bash

# This gets vmName, vmRAM, vmDisk, ip address of host, ip address of user
# We want to create a virtual machine on the host with name vm_name
# We will ssh into the host and run the create commands
# This script will output the IP of the VM created
# disa_server can only be accessed throu

vmName="${1}_${5}"
diskSize=$3
ramSize=$2
vmCore=core
# Cloning commands
ssh disa_server@$4 sudo virsh dumpxml "$vmCore" > createnewdisavm.xml
uuidNew="$(ssh disa_server@$4 uuidgen)"
#### Editing the XML file ####
# checking for ram changes
ramSize="$2"
if [ "$ramSize" = "" ]; then
	ramSize=1024
fi
ramSize=$(echo $(($ramSize*1024)))
addr="'\/home\/disa_server\/kvm-pool\/$vmName.qcow2'\/>"
ssh disa_server@$4 sudo sed -i -e "s/\(<name>\).*/\1$vmName<\/name>/" \
	-e "s/\(<uuid>\).*/\1$uuidNew<\/uuid>/" \
	-e "s/\(unit='KiB'>\).*/\1$ramSize<\/memory>/" \
	-e "s/\(<currentMemory unit='KiB'>\).*/\1$ramSize<\/currentMemory>/" \
	-e "s/\(<source file=\).*/\1$addr/" createnewdisavm.xml
#Copying and resizing the hard-disk
echo "Copying the hard-disk"
ssh disa_server@$4 sudo cp "/home/disa_server/kvm-pool/$vmCore.qcow2" "/home/disa_server/kvm-pool/$vmName.qcow2"
# diskSize="$3"
if [ "$diskSize" = "" -o "$diskSize" = "5G" ]
then
	echo "Hard Disk attached!"
else
	required=${diskSize%G*}
	resize=$(( $required - 5 ))
	ssh disa_server@$4 sudo qemu-img resize -f raw "/home/disa_server/kvm-pool/$vmName.qcow2" +$resize"G"
fi 


# after all editing is done
ssh disa_server@$4 sudo virsh define createnewdisavm.xml
echo "Eureka! $vmName created!"
ssh disa_server@$4 sudo rm -f createnewdisavm.xml # for removing file after creation


#This script return the ip address of the vm whose name is given as argument
dump=$(ssh disa_server@$4 virsh dumpxml $vmName | grep "mac addr")
mac=$(echo $dump | cut -f 2 -d "'")
ip=$(ssh disa_server@$4 arp -n | grep  $mac | cut -f 1 -d " ")

echo $ip