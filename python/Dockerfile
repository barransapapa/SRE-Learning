FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask requests opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-flask opentelemetry-exporter-otlp-proto-grpc opentelemetry-instrumentation-wsgi opentelemetry-instrumentation-logging opentelemetry-exporter-otlp prometheus_client
COPY . .
# Create logs directory with full permissions
RUN mkdir -p /app/logs
RUN chmod -R 777 /app/logs
CMD ["flask", "run", "--host", "0.0.0.0"]

#This file allows docker to install all dependencies and run the flask application in a containerized environment.