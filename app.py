from flask import Flask
import logging

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

logging.basicConfig(level=logging.INFO)

trace_provider = TracerProvider()
trace.set_tracer_provider(trace_provider)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector.monitoring:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    return "Hello from OpenTelemetry Python!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)