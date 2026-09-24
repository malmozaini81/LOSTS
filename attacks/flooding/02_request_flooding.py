"""test: repeated forged LOSTS requests.
This intentionally uses a conservative finite rate/count so it can measure handling
without becoming an uncontrolled denial-of-service tool.
"""
import socket, secrets, time
from config import ADMIN_IP, OTA_PORT

DEVICE_MAC = "90E5B1CC2DB8"
MISSING = "00000124"
COUNT = 50          # finite test
RATE_PER_SEC = 5    # conservative default

interval = 1.0 / RATE_PER_SEC
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    start = time.perf_counter()
    for i in range(COUNT):
        forged_sig = secrets.token_hex(64).upper()
        payload = f"LOSTS:{DEVICE_MAC}:{MISSING}:{forged_sig}".encode("ascii")
        s.sendto(payload, (ADMIN_IP, OTA_PORT))
        time.sleep(interval)
    elapsed = time.perf_counter() - start

print(f"Sent {COUNT} forged requests in {elapsed:.2f}s (~{COUNT/elapsed:.2f} req/s).")
print("Measure on administrator: CPU usage, verification count/time, OTA latency, and rebroadcast count.")
print("Expected security result: invalid signatures do not trigger CHUNK rebroadcasts.")
