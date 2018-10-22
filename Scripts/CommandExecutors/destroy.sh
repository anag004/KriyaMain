# This script destroys the VM on the remote guest



ssh disa_server@$2 virsh undefine "$1_$3" --remove-all-storage; rm /home/disa_server/kvm-pool/"$1_$3.qcow2"