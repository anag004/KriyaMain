#!/bin/bash

# This command resumes the virtual machine takes input vmName, hostIP, userIP

ssh disa@$2 virsh resume $vmName_$3
