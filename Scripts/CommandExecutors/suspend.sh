#!/bin/bash

# This command suspends the virtual machine takes input vmName, hostIP, userIP

ssh disa@$2 virsh suspend "$1_$3"
