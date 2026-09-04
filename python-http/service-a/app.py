from flask import Flask, request, jsonify
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)
SERVICE = "A"


def log_request(endpoint: str, status: str, start: float) -> None:
    latency_ms = int((time.time() - start) * 1000)
    logging.info(
        f"service={SERVICE} endpoint={endpoint} status={status} latency_ms={latency_ms}"
    )


@app.get("/health")
def health():
    start = time.time()
    log_request("/health", "ok", start)
    return jsonify(status="ok")


@app.get("/echo")
def echo():
    start = time.time()
    msg = request.args.get("msg", "")
    log_request("/echo", "ok", start)
    return jsonify(echo=msg)


if __name__ == "__main__":
    logging.info("service=A listening on http://127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080)
