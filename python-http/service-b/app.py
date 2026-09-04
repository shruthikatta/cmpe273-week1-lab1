from flask import Flask, request, jsonify
import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = Flask(__name__)
SERVICE = "B"
SERVICE_A = "http://127.0.0.1:8080"
# Hard timeout so Service B fails fast when A is slow or unreachable
CALL_TIMEOUT_SEC = 1.0


def log_request(endpoint: str, status: str, start: float, error: str | None = None) -> None:
    latency_ms = int((time.time() - start) * 1000)
    if error:
        logging.error(
            f'service={SERVICE} endpoint={endpoint} status={status} '
            f'error="{error}" latency_ms={latency_ms}'
        )
    else:
        logging.info(
            f"service={SERVICE} endpoint={endpoint} status={status} latency_ms={latency_ms}"
        )


@app.get("/health")
def health():
    start = time.time()
    log_request("/health", "ok", start)
    return jsonify(status="ok")


@app.get("/call-echo")
def call_echo():
    start = time.time()
    msg = request.args.get("msg", "")
    try:
        r = requests.get(
            f"{SERVICE_A}/echo",
            params={"msg": msg},
            timeout=CALL_TIMEOUT_SEC,
        )
        r.raise_for_status()
        data = r.json()
        log_request("/call-echo", "ok", start)
        return jsonify(service_b="ok", service_a=data)
    except requests.exceptions.Timeout as e:
        log_request("/call-echo", "error", start, error=f"timeout: {e}")
        return jsonify(
            service_b="ok",
            service_a="unavailable",
            error=f"timeout calling Service A after {CALL_TIMEOUT_SEC}s",
        ), 503
    except Exception as e:
        log_request("/call-echo", "error", start, error=str(e))
        return jsonify(
            service_b="ok",
            service_a="unavailable",
            error=str(e),
        ), 503


if __name__ == "__main__":
    logging.info("service=B listening on http://127.0.0.1:8081")
    app.run(host="127.0.0.1", port=8081)
