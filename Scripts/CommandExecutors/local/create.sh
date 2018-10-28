#!/bin/bash
# This script resides on the guest. Takes in input as vmName, vmRam, vmDisk and creates a VM

vmCore=core
vmName="$1"
diskSize="$3"
ramSize="$2"

# Cloning commands
sudo virsh dumpxml "$vmCore" > createnewdisavm.xml
uuidNew="$(uuidgen)"
#### Editing the XML file ####
# checking for ram changes
ramSize="$2"
if [ "$ramSize" = "" ]; then
	ramSize=1024
fi
ramSize=$(echo $(($ramSize*1024)))
addr="'\/home\/disa_server\/kvm-pool\/$vmName.qcow2'\/>"
sudo sed -i -e "s/\(<name>\).*/\1$vmName<\/name>/" \
	-e "s/\(<uuid>\).*/\1$uuidNew<\/uuid>/" \
	-e "s/\(unit='KiB'>\).*/\1$ramSize<\/memory>/" \
	-e "s/\(<currentMemory unit='KiB'>\).*/\1$ramSize<\/currentMemory>/" \
	-e "s/\(<source file=\).*/\1$addr/" createnewdisavm.xml
#Copying and resizing the hard-disk
echo "Copying the hard-disk"
sudo cp "/home/disa_server/kvm-pool/$vmCore.qcow2" "/home/disa_server/kvm-pool/$vmName.qcow2"
chmod 777 "/home/disa_server/kvm-pool/$vmName.qcow2"
diskSize="$3"
if [ "$diskSize" = "" -o "$diskSize" = "5G" ]
then
	echo "Hard Disk attached!"
else
	required=${diskSize%G*}
	resize=$(( $required - 5 ))
	sudo qemu-img resize -f raw "/home/disa_server/kvm-pool/$vmName.qcow2" +$resize"G"
fi 

# after all editing is done
sudo virsh define createnewdisavm.xml
echo "Eureka! $vmName created!"
sudo rm -f createnewdisavm.xml # for removing file after creation
