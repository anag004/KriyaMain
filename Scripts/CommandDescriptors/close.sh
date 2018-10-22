#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}close"
echo "${normal}This will remove all VMs and exit the Kriya interface."
echo "${bold}WARNING: Running this command will permanently delete all VMs and the data inside them.${normal}"
