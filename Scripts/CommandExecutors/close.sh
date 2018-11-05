vmName="$1"
ssh disa_server@$2 virsh shutdown $vmName

ssh disa_server@$2 virsh undefine "$1_$3" --remove-all-storage; rm -f /home/disa_server/kvm-pool/"$1_$3.qcow2"