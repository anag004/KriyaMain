#!/bin/bash

# This command sets up the user disa_server with sudo privileges on a computer needed for the VMs to run.
# The password of this will be asdf
# Another test user will be created which will NOT have admin privileges and will be used to ssh into the VM
# The ubuntu install iso should be present here
# This script must be run as a sudo
# Installation KVM and QEMU
# Creation of virtual bridge network
# Creation of directories kvm-pool
# This takes the ip address of the user as input

#Tested: Works

vmName=core

sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils virt-manager
sudo useradd -m disa_server
sudo mkdir /home/disa_server/kvm-pool
sudo useradd -m disa_user
echo "disa_server:asdf" | sudo chpasswd
echo "disa_user:asdf" | sudo chpasswd
sudo usermod -a -G sudo disa_server
sudo usermod -aG libvirtd disa_server
sudo virsh net-create createnetwork.xml
sudo virsh pool-define-as $vmName dir - - - - /home/disa_server/kvm-pool/
sudo virsh pool-build $vmName
sudo virsh pool-start $vmName
sudo virsh pool-autostart $vmName
sudo qemu-img create -f raw /home/disa_server/kvm-pool/$vmName.qcow2 5G
sudo rm -rf ~/.cache/virt-manager/
sudo virt-install --name=$vmName --ram 1024 --vcpu=1 -c ~/kvm-isos/ubuntu16-server-unattended-install.iso --os-type=linux --os-variant=generic --disk path=/home/disa_server/kvm-pool/$vmName.qcow2 --graphics spice --network bridge=virbr0
sudo chmod 755 /home/disa_server/kvm-pool

# PROBLEMS::: ssh keys must be created
# MANUAL COMMANDS:
# 1. Copy keygens from the server to the guest computer to enable passwordless login
