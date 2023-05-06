#! /bin/bash
if [ -d "/domino/edv/european-customer-data" ] 
then
    echo "Directory /domino/edv/european-customer-data exists."
    ln -s "/domino/edv/european-customer-data" "/mnt/data2" 
elif [ -d "/domino/edv/canadian-customer-data" ]
then
    echo "Directory /domino/edv/canadian-customer-data exists."
    ln -s "/domino/edv/canadian-customer-data" "/mnt/data2"
elif [ -d "/domino/edv/southeast-asia-customer-data" ]
then
    echo "Directory /domino/edv/southeast-asia-customer-data exists."
    ln -s "/domino/edv/southeast-asia-customer-data" "/mnt/data2"
else
    echo "Error: External Volume not added - speak to your instructor"
fi