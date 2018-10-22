# This is a wrapper for the connect.py script
# Takes input as the value of the ip address of the host

connectport=$( python connect.py $1 )

echo $connectport

ncat "$1" "$connectport"