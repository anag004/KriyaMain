#!/bin/bash

# This script runs on the host
# This command starts the virtual machine takes input vmName, hostIP, userIP

ssh -t disa_server@$2 "sudo bash /home/dhull/DISA/Scripts/CommandExecutors/local/start.sh \"$1_$3\" "
