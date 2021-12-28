import logging
from flask import Flask, render_template, request, jsonify
from jaeger_client import Config
from opentracing.ext import tags
from opentracing.propagation import Format
import pymongo
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer('backend')

app = Flask(__name__)

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)


@app.route("/")
def homepage():
    with tracer.start_span('homepage') as span:
        span.set_tag('response', 'Hello World')
        return "Hello World"


@app.route("/api")
def my_api():
    with tracer.start_span('api') as span:
        answer = "something"
        span.set_tag('response', answer)
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span('star') as span:
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        with tracer.start_span('insert') as span:
            star_id = star.insert({"name": name, "distance": distance})
            span.set_tag('star_id', star_id)
            with tracer.start_span('find') as span:
                new_star = star.find_one({"_id": star_id})
                output = {"name": new_star["name"], "distance": new_star["distance"]}
                span.set_tag('star_name', new_star["name"])

                return jsonify({"result": output})


if __name__ == "__main__":
    app.run()
