#!/bin/bash

cd $(dirname "$0")
echo -n "Enter your NASA API key to build the app environment: "
read -s apiKey
echo
echo "Your API key is $apiKey"
kubectl apply -f ../k8s/nasa_namespace.yaml
kubectl create secret generic nasa-api-key --from-literal=apiKey=$apiKey -n nasa
kubectl apply -f ../k8s/deployment.yaml
kubectl apply -f ../k8s/service.yaml