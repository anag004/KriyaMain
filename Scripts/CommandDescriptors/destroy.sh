#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}destroy <vm-name>"
echo "${bold}WARNING: ${normal}This command will irreversibly delete a VM and all the data contained within it."
