# CMPE 273 – Week 1 Lab 1: First Distributed System

**Track chosen:** `python-http/` (Flask + requests)

Two independent HTTP services that talk over the network:

| Service | Port | Endpoints |
|---------|------|-----------|
| **Service A** (Echo) | `8080` | `GET /health`, `GET /echo?msg=...` |
| **Service B** (Client) | `8081` | `GET /health`, `GET /call-echo?msg=...` → calls Service A |

Service B uses a **1-second timeout** when calling A. If A is down or slow, B returns **HTTP 503** and logs the error.

---

## How to run locally

Requires **Python 3.10+**.

### Terminal 1 — Service A

```bash
cd python-http/service-a
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Terminal 2 — Service B

```bash
cd python-http/service-b
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Quick checks

```bash
curl "http://127.0.0.1:8080/health"
curl "http://127.0.0.1:8081/health"
curl "http://127.0.0.1:8080/echo?msg=hello"
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

---

## Success proof

With both services running:

```bash
$ curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:8080/health"
{"status":"ok"}
HTTP 200

$ curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:8081/health"
{"status":"ok"}
HTTP 200

$ curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:8080/echo?msg=hello"
{"echo":"hello"}
HTTP 200

$ curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:8081/call-echo?msg=hello"
{"service_a":{"echo":"hello"},"service_b":"ok"}
HTTP 200
```

Example Service B log (success):

```text
service=B endpoint=/call-echo status=ok latency_ms=5
```

---

## Failure proof (independent failure)

Stop Service A (Ctrl+C in Terminal 1), leave Service B running, then:

```bash
$ curl -s -w "\nHTTP %{http_code}\n" "http://127.0.0.1:8081/call-echo?msg=hello"
{"error":"HTTPConnectionPool(host='127.0.0.1', port=8080): Max retries exceeded with url: /echo?msg=hello (Caused by NewConnectionError(\"HTTPConnection(host='127.0.0.1', port=8080): Failed to establish a new connection: [Errno 61] Connection refused\"))","service_a":"unavailable","service_b":"ok"}
HTTP 503
```

Example Service B log (failure):

```text
service=B endpoint=/call-echo status=error error="...Connection refused..." latency_ms=0
GET /call-echo?msg=hello HTTP/1.1" 503
```

Service B stays up and returns a clear 503 — A’s crash does not take B down with it.

---

## What makes this distributed?

This system is distributed because Service A and Service B are **separate processes** that communicate only over the **network** (HTTP on localhost), not by sharing memory or a single address space. Each service can start, stop, fail, and scale independently: when A is unreachable, B still runs, detects the failure via a timed-out/refused connection, logs it, and returns 503 to the client. That independent failure and network-bound collaboration is the core property of a distributed system — even when both processes happen to run on the same machine.

---

## Project layout

```text
python-http/
  service-a/app.py          # Echo service (:8080)
  service-b/app.py          # Client that calls A (:8081)
go-http/                    # Optional Go track (from starter; not used for this submission)
docs/                       # Lab brief from Canvas
```
