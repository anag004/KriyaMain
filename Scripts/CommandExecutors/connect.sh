

# This script opens up a new terminal with a ssh connection to the VM. 
# Takes vmName, hostIP, ipaddr of user, vmIP as input
# This script runs on the user

sshpass -p 'asdf' ssh -t disa_user@$2 sshpass -p 'asdf' ssh -t ubuntu@$4

# 'asdf' will be the password of the disa_user

