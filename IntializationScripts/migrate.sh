#!/bin/bash
# This script will first copy the hard drive of a vm + it's configuration file and then create vm on anothermachine rather than direct migrating!
# This script will be called by the server. and the script will be present in the home directory of host's disa_server.

vmName="$1"
ramSize=$(virsh dumpxml "$vmName" | grep "currentMemory"| cut -d">" -f2 | cut -d"<" -f1)
newIP="$2"

x=$(virsh list --all | grep $vmName | wc -l)
if [[ x -lt 1 ]]; then
	echo "$vmName doesn't exist!";exit 0;
fi
# shutdown first!
x=$(virsh list | grep $vmName | wc -l)
if [[ x -gt 0 ]]; then
	virsh shutdown "$vmName";sleep 10;
fi
# make it cross computer! 
# copy xml as well
scp /home/disa_server/kvm-pool/"$vmName".qcow2 disa_server@"$newIP":/home/disa_server/kvm-pool/"$vmName".qcow2
# after all editing is done
sshpass -p 'asdf' ssh -t disa_server@$newIP 'sudo bash /home/disa_server/editxmlmigration.sh' $vmName $ramSize 
# destroy the original vm after that.
virsh undefine "$vmName"	
sudo rm /home/disa_server/kvm-pool/$vmName.qcow2
 # for removing file after creation
