FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask requests opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-flask opentelemetry-exporter-otlp-proto-grpc opentelemetry-instrumentation-wsgi opentelemetry-instrumentation-logging opentelemetry-exporter-otlp
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
