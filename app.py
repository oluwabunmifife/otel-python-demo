from flask import Flask
import logging

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenTelemetry
trace_provider = TracerProvider()
trace_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector.monitoring:4317")))
FlaskInstrumentor().instrument()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from OpenTelemetry Python!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)