#!/bin/bash
# This script shuts down the vm gracefully.
# Inputs: vmName, hostIP

vmName="$1"
ssh disa_server@$2 virsh shutdown $vmName

