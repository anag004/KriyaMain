#!/bin/bash

# Stores formatting
bold=$(tput bold)
normal=$(tput sgr0)

echo "${bold}resume <vm-name>"
echo "${normal}This command will resume a suspended VM."
