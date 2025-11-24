#!/bin/bash

# Navigate to the directory of the script
cd $(dirname "$0")
# Prompt the user for their NASA API key
echo -n "Enter your NASA API key to build the app environment: "
# Save the input as a variable without echoing it to the terminal
read -s apiKey
echo
# Apply Kubernetes configurations and deploy the application using Ansible
ansible-playbook -i ../ansible/inventory.ini ../ansible/ansible_remove.yaml
ansible-playbook -i ../ansible/inventory.ini ../ansible/ansible_nasa_namespace.yaml
kubectl create secret generic nasa-api-key --from-literal=apiKey=$apiKey -n nasa
ansible-playbook -i ../ansible/inventory.ini ../ansible/ansible_deploy.yaml
# Notify the user of completion
echo "Nasa app environment build complete."