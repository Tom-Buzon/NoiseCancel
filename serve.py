#!/usr/bin/env python3
"""
ANC Lab V0 - tiny static server.

HTTP:
  python serve.py

HTTPS:
  python serve.py --https cert.pem key.pem

Then open the printed URL from a device on the same Wi-Fi.
Important: browser microphone access requires a secure context.
"""
import argparse
import http.server
import socket
import ssl
from pathlib import Path

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, default=8000)
p.add_argument("--https", nargs=2, metavar=("CERT", "KEY"))
args = p.parse_args()

root = Path(__file__).resolve().parent
handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(root), **kw)
server = http.server.ThreadingHTTPServer(("0.0.0.0", args.port), handler)

scheme = "http"
if args.https:
    cert, key = args.https
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=cert, keyfile=key)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    scheme = "https"

ip = lan_ip()
print()
print("ANC Lab V0")
print(f"Local PC : {scheme}://localhost:{args.port}")
print(f"Wi-Fi    : {scheme}://{ip}:{args.port}")
print()
if scheme == "http":
    print("NOTE: tone generation works over HTTP, but phone microphone access is normally blocked on a LAN IP.")
    print("Use trusted HTTPS (see README) or open index.html locally on the phone for the microphone test.")
print("Ctrl+C to stop.")
print()
server.serve_forever()
