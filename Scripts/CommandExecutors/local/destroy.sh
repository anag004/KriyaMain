#!/bin/bash
# This script will destroy the VM and delete it's directory too!
vmName="$1"
virsh undefine $vmName
sudo rm /home/disa_server/kvm-pool/$vmName.qcow2

