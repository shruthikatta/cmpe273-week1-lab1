# Python HTTP Track (Week 1)

See the root [README.md](../README.md) for full run instructions, success/failure proof, and the “What makes this distributed?” write-up.

## Quick start

**Service A** (port 8080):

```bash
cd service-a
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Service B** (port 8081, new terminal):

```bash
cd service-b
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Test:**

```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

Stop Service A and rerun the curl to observe HTTP 503 + error logging.
