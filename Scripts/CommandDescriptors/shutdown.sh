#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)
echo "${bold}shutdown <vm-name>"
echo "${normal}This command forcefully powers off the virtual machine. To gracefully shutdown the virtual machine connect to it and run the command:"
echo "sudo shutdown -h now"


