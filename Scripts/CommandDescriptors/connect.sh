#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}connect <vm-name>"
echo "${normal}This will open up a new terminal window with an ssh connection to the VM."
