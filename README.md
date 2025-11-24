# SRE-Learning
This is a repository for my SRE academy training.

### Project
This python app requests to the NASA NeoWs API to retrieve data for a specific date, to get data about asteroids that are close to the Earth. To get this app working, a NASA API key is required, which can be requested [here](https://api.nasa.gov/).

### Deployment
The python script retrieves the asteroids information, and can be checked on the asteroids endpoint:
<img width="1909" height="836" alt="image" src="https://github.com/user-attachments/assets/bacb1540-a538-4558-8734-6fa8de926394" />

The code of this python app can be found on this repository, inside the python directory, but it's also available at [docker hub](https://hub.docker.com/repository/docker/barransapapa/nasa-app/general), which is used on the deployment.yaml to create the kubernetes deployment that runs the main app. This app features Flask to enable web server functions and Opentelemetry to collect all the metrics data that is sent to Prometheus and Jaeger.


As this python script runs into a K8s deployment, a Dockerfile is included to install into the container libraries like flask, requests, several opentelemetry libraries needed for data scraping and the prometheus_client library.

To get this aplication sending data to Prometheus and Jaeger, a cronjob is running every two minutes, to get new data for Prometheus and Jaeger:

<img width="799" height="188" alt="image" src="https://github.com/user-attachments/assets/32428d54-06ef-41fb-97d6-6ab52179e409" />

Latency to retrieve the asteroids data is calculated on this app, to send the information to the tools used on this project.

### Prometheus

Prometheus is used on this project to collect and store metrics. As well, it's used to expose the metrics collected on the app to expose them to Grafana. This is how the Prometheus UI looks once it was connected to nasa-app

<img width="1899" height="1061" alt="image" src="https://github.com/user-attachments/assets/3ebd9df5-85ca-48dc-9f99-64faeb75d99c" />

### cAdvisor

cAdvisor is also included on this project, to retrieve metrics data about the pod that is running the python application.

### OpenTelemetry

OpenATelemetry is used on this project to send the collected data to jaeger

### Jaeger

Data sent by openTelemetry, which is every call made by the app to NASA API, can be seen on Jaeger, specifically the duration of each call:

<img width="1915" height="1073" alt="image" src="https://github.com/user-attachments/assets/9afbf69f-cbf7-487b-9b15-cb0d30f33ab7" />


### Grafana
On Grafana, dashboards related to the metrics collected on the app are displayed. There are two dashboards, the App Dashboard that shows the CPU Usage and Pod CPU Usage of the host running the application. As well, a graph to show the error logs for Nasa Appis defined:

<img width="1908" height="899" alt="image" src="https://github.com/user-attachments/assets/20e3411e-a1a9-4e78-bc14-aa3c319ca97a" />

Also, there is a golden signals dashboard that show data about Latency, Traffic and Saturation:
<img width="1903" height="1061" alt="image" src="https://github.com/user-attachments/assets/5f8c0a57-602b-4ec4-a12f-cbb00ca0cff9" />

As well, three alerts are defined, an alert that triggers if the latency of the endpoint is below 1400 miliseconds, as well as an alert that nchecks if the received bytes are lower than 1 byte. Also, an alert to check that there are less than two errors on the app is featured:

<img width="1913" height="1072" alt="image" src="https://github.com/user-attachments/assets/bf14d2ff-bf33-4091-ae13-9d5e1ca1bcf4" />

### Automation to deploy the app

A bash Script is included on this repository to deploy the kubernetes resources on your computer. This bash script asks to the user for the NASA API key, which is required by the application pods, to generate the API calls. Once you provide your API key, three ansible playbooks are executed: ansible_remove, in case that there are k8s resources using required namespaces, ansible_nasa_namespace, which creates the nasa namespace required for the app, and ansible_deploy, which creates all the required resources for this app to work

<img width="1905" height="1080" alt="image" src="https://github.com/user-attachments/assets/b9e833e0-b311-4246-9b71-26362183a917" />

