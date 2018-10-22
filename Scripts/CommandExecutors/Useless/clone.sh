#!/bin/bash

###NOT ANY USE NOW###

# This gets vmName, vmRAM, vmDisk, ip address of host, ip address of user
# We want to create a virtual machine on the host with name vm_name
# We will ssh into the host and run the create commands
# This script will output the IP of the VM created

# We first clone a VM with 1GB of RAM and 10GB of hard disk space
# We modify memory and attach hard disks as needed

sudo virt-clone --original "core" --name $vmName --auto-clone

if ![ $1 -eq 10 ]
then
	mkdir /home/disa_server/kvm-pool/$vmName
	sudo qemu-img create -f raw /home/disa_server/kvm-pool/$vmName/${vmName}Aux.qcow2 ${3}G 
	sudo virsh attach-disk $vmName /home/disa_server/kvm-pool/$vmName/${vmName}Aux.qcow2 vdb --cache none  	
fi 

dump=$(virsh dumpxml $vmName | grep "mac addr")
mac=$(echo $dump | cut -f 2 -d "'")
ip=$(arp -n | grep $mac | cut -f 1 -d " ")
echo $ip

# COPY THE KEYS USING SSHPASS
