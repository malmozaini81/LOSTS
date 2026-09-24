"""Test: forged LOSTS recovery request.
Expected: administrator rejects request and does NOT rebroadcast requested chunks.
"""
import socket, secrets
from config import ADMIN_IP, OTA_PORT

DEVICE_MAC = "90E5B1CC2DB8"
MISSING = "00000033,00000083,000000D4,00000124,000001C7,00000218,00000269"
# P-256 raw signature is 64 bytes = 128 hex chars. Random bytes cannot verify.
FORGED_SIG = secrets.token_hex(64).upper()
payload = f"LOSTS:{DEVICE_MAC}:{MISSING}:{FORGED_SIG}".encode("ascii")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(payload, (ADMIN_IP, OTA_PORT))
print(f"Sent forged LOSTS ({len(payload)} bytes) to {ADMIN_IP}:{OTA_PORT}")
print("Expected: signature verification fails; no CHUNK rebroadcast is triggered.")
