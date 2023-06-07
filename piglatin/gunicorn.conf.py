import os
import multiprocessing

PORT = os.environ.get('PORT')

bind = f"0.0.0.0:{PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
statsd_host = "statsd-exporter:9125"
statsd_prefix = "flask_app"
reload = os.environ.get("DEBUG", False).lower() == "true"

logconfig = "/app/logging.conf"
