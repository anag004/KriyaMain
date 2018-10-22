#!/bin/bash
# This script will be run on the server to find the ip that can run the VM
# Command line arguments: Required RAM is input argument ($1 in MB)

declare -a IPs=("10.194.2.145")
ram=$(( $1 * 1048/1000 ))
for i in "${IPs[@]}"
do
    val=$(sshpass -p 'asdf' ssh -q -t disa_server@"$i" 'bash $HOME/checkfree.sh' $ram)
    compare=$( echo $'1\r' )
    if [ "$val" == "$compare" ]; then
    echo "FOUND $i"; exit 1
    # exit the script, return the ip
    elif [ "$val" == "" ]; then
            echo "NCONFIG $i"
    fi
done

echo "BUSY"
# can make a resource handling side script as well.