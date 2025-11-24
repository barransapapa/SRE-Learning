import requests
import random
import time
from datetime import date
from flask import Flask, Response
from os import getenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

from prometheus_client import generate_latest, Counter, Histogram, Gauge

import logging
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs/sre-app.log', encoding='utf-8', level=logging.DEBUG)
logger.debug('This message should go to the log file with debug level')
logger.info('This message should go to the log file with info level')
logger.warning('This message should go to the log file with warning level')
logger.error('This message should go to the log file with error level')

# Set up OpenTelemetry tracing with my service name
#resource = Resource(attributes={"service.name": "nasa-app-service"})
resource = Resource.create({"service.name": "nasa-app-service"})

span_exporter = OTLPSpanExporter(endpoint="otel-collector.opentelemetry.svc.cluster.local:4317", insecure=True)

tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
log_exporter = OTLPLogExporter(endpoint="otel-collector.opentelemetry.svc.cluster.local:4317", insecure=True)
log_processor = BatchLogRecordProcessor(log_exporter)
logger_provider.add_log_record_processor(log_processor)
otel_handler = LoggingHandler(logger_provider=logger_provider)
logging.getLogger().addHandler(otel_handler)

# This is a simple Flask web application that provides an endpoint to retrieve data about asteroids from NASA's NeoWs API.
# Initialize Flask app
app = Flask(__name__)


FlaskInstrumentor().instrument_app(app)
app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)

#Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])

@app.route('/') #These are the paths on the link
def go_to_asteroids():
    return 'Please go to the /asteroids endpoint to see data about asteroids from NASA NeoWs API.'


#This endpoint retrieves data about asteroids from NASA's NeoWs API
@app.get('/asteroids') #http://127.0.0.1:5000/asteroids
def get_asteroids():
    #Get today's date in YYYY-MM-DD format
    search_date=date.today().strftime("%Y-%m-%d")
    #Retrieve the NASA API key from environment variables. The line below gets a secret from the environment to use as API key. You can get your own API key by registering at https://api.nasa.gov/.
    api_key = getenv("NASA_API_KEY")
    #Make a GET request to the NASA NeoWs API to retrieve asteroid data for the specified date
    start_timer = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/asteroids').inc()
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={search_date}&end_date={search_date}&api_key={api_key}"
    latency = time.time() - start_timer
    REQUEST_LATENCY.labels(method='GET', endpoint='/asteroids').observe(latency)
    response = requests.get(url)
    data = response.json()
    with tracer.start_as_current_span("process_asteroid_data"):
        return {"data": data}
    
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    import os
    logs_dir = './logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    app.run(host='0.0.0.0',port=5000)

# Reference: https://apidog.com/es/blog/how-to-use-nasa-api-3/#servicio-web-de-objetos-cercanos-a-la-tierra-neows
# for date, asteroids in data ["near_earth_objects"].items():
#     print(f"Asteroids on {date}:")
#     for asteroid in asteroids: 
#         print(f"- {asteroid['name']}: It was close to the earth: {asteroid['is_potentially_hazardous_asteroid']}, Velocity: {asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")
