#!/bin/bash

# This script requires `gcloud` cli
# https://cloud.google.com/sdk/docs/install-sdk

if [[ -z "$1" ]]
then
    echo "Usage: ./ssh.sh <instance-name>"
    exit 1
fi

# !!!!!!!!! CHANGE THIS !!!!!!!!!
YOUR_SSH_KEY_PATH=~/.ssh/id_pdd
# !!!!!!!!! CHANGE THIS !!!!!!!!!

instance=$1
ip=$(gcloud compute instances list --filter="name=${instance}" --format="get(networkInterfaces[0].accessConfigs[0].natIP)")

if [[ -z "$ip" ]]
then
    echo "Instance not found"
    echo "Check if the instance is running"
    exit 1
fi

if [[ "$instance" == "driver" ]]
then
    ADDITONAL_ARGS="-L 8888:localhost:8888"
elif [[ "$instance" == "master" ]]
then
    ADDITONAL_ARGS="-D 1080"
else
    ADDITONAL_ARGS=""
fi

ssh $ip -o 'IdentitiesOnly yes' -i "$YOUR_SSH_KEY_PATH" $ADDITONAL_ARGS
