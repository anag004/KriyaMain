#!/bin/bash
# This script will first copy the hard drive of a vm + it's configuration file and then create vm on anothermachine rather than direct migrating!
# This script will be called by the server.

vmName="$1"
sudo virsh dumpxml "$vmName" > migratevm.xml
newIP="$2"
#Copying and resizing the hard-disk
# echo "Copying the hard-disk"

# make it cross computer! 
# copy xml as well
scp migratevm.xml disa_server@"$newIP":~/
scp /home/disa_server/kvm-pool/"$vmName".qcow2 disa_server@"$newIP":/home/disa_server/kvm-pool/"$vmName".qcow2
sudo rm -f migratevm.xml
# after all editing is done
ssh -t disa_server@$newIP 'sudo virsh define ~/migratevm.xml
sudo rm -f migratevm.xml'
 # for removing file after creation
