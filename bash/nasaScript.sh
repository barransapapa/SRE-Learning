#!/bin/bash

# Navigate to the directory of the script
cd $(dirname "$0")
# Prompt the user for their NASA API key
echo -n "Enter your NASA API key to build the app environment: "
# Save the input as a variable without echoing it to the terminal
read -s apiKey
echo
# Apply Kubernetes configurations
kubectl apply -f ../k8s/nasa_namespace.yaml
kubectl create secret generic nasa-api-key --from-literal=apiKey=$apiKey -n nasa
kubectl apply -f ../k8s/deployment.yaml
kubectl apply -f ../k8s/service.yaml