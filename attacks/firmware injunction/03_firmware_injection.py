"""Test: unauthorized firmware HEADER injection.
Uses the captured HEADER fields but replaces the ECDSA signature with a random one.
Expected: ESP32-S3 rejects the HEADER, so injected firmware is never accepted.
"""
import socket, secrets
from config import BROADCAST_IP, OTA_PORT

header_unsigned = (
    "HEADER:192.168.0.94:2CCA160335E1:0000000E:000D40D0:0000026D:0578:"
    "20645cf9631b48c5fa38dc753ac0e4120180ed2e03ff43540d0758362ee3d903"
)
forged_sig = secrets.token_hex(64).lower()
payload = f"{header_unsigned}:{forged_sig}".encode("ascii")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(payload, (BROADCAST_IP, OTA_PORT))
print(f"Broadcast forged HEADER to {BROADCAST_IP}:{OTA_PORT}")
print("Expected: ECDSA verification fails and the update is not initialized.")
