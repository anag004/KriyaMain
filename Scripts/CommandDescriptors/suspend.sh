#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}suspend <vm-name>"
echo "${normal}This command will temporarily halt the running VM and keep its state frozen. This can be resumed later with the ${bold}resume${normal} command."
