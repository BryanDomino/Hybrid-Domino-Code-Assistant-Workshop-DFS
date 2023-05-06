#! /bin/bash
if [ -d "/mnt/data" ]
then
    sudo unlink "/mnt/data"
fi
if [ -d "/domino/edv/aws-west-data" ] 
then
    echo "Directory /domino/edv/aws-west-data exists."
    sudo ln -s "/domino/edv/aws-west-data" "/mnt/data" 
elif [ -d "/domino/edv/azure-canada-files" ]
then
    echo "Directory /domino/edv/azure-canada-files exists."
    sudo ln -s "/domino/edv/azure-canada-files" "/mnt/data"
elif [ -d "/domino/edv/aws-ireland-data" ]
then
    echo "Directory /domino/edv/aws-ireland-data exists."
    sudo ln -s "/domino/edv/aws-ireland-data" "/mnt/data"
else
    echo "Error: External Volume not added - speak to your instructor"
fi