#!/bin/bash

# ./create-topics.sh [bootstrap server] [topic_1] [topic_2] [topic_3] ...

BOOTSTRAP_SERVER=$1
shift

echo "Creating kafka topics..."
for topic in "$@"; do
    kafka/bin/kafka-topics.sh --create --bootstrap-server $BOOTSTRAP_SERVER --topic $topic
done
