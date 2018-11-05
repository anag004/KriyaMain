#!/bin/bash
#!/bin/sh

# This script runs on the server and calls a remote script on the host which creates the virtual machine
# Takes as input vmName, vmRAM, vmDisk, freeHostIP, ipaddress of user requesting the machine

ssh -t disa_server@$4 "sudo bash /home/disa_server/DISA/Scripts/CommandExecutors/local/create.sh \"$1_$5\" \"$2\" \"$3\""

