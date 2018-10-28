#!/bin/bash
# This script will be run on the server to find the ip that can run the VM
declare -a IPs=("localhost" "127.0.0.1")
ram=$(($1 * 1048/1000 ))
for i in "${IPs[@]}"
do
    val=$(echo $(sshpass -p 'asdf' ssh -t disa_server@"$i" 'bash $HOME/checkfree.sh' $ram ))
    compare=$(echo $'1\r')
    if [ "$val" == "$compare" ]; then
    echo $i; exit 1
    # exit the script, return the ip
    fi
done
echo "All Machines are currently busy! Please try again later!"
# can make a resource handling side script as well.