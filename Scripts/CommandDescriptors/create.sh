#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)
echo "${bold}create <vm-name> <size of RAM in MB> <hard disk space in GB>"
echo "${normal}This command requests a virtual machine be created. The name of the virtual machine must be unique and consist of ${bold}alphanumeric characters only${normal}. This name will be used as an argument in commands to refer to the VM. Upon running this command, a virtual machine with a standard Ubuntu Server 18.04 will be created. For a proper install keep the hard disk size atleast 8GB."


