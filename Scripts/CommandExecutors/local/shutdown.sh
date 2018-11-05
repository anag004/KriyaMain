#!/bin/bash
vmName="$1"
virsh shutdown $vmName

# sleep 10

# virsh destroy $vmName