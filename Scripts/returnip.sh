 #!/bin/bash

# This script calls the local returnip script
# Inputs are vmName, hostIp, userip 

vmName="$1_$3"
ssh -t disa_server@$2 "bash /home/disa_server/DISA/Scripts/CommandExecutors/local/returnip.sh $vmName"