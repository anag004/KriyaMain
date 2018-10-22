#!/bin/bash

myinput = $( ncat --listen -p 6000 )

echo DONE

echo "$myinput"
