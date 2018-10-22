#!/bin/bash

# This command suspends the virtual machine takes input vmName, hostIP, userIP

ssh disa@$2 virsh suspend $vmName_$3
