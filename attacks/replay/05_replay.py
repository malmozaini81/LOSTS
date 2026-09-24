"""Test: replay a previously captured valid LOSTS request.
Expected with the current design: signature remains valid and may trigger redundant rebroadcast traffic.
"""
import socket
from config import ADMIN_IP, OTA_PORT

CAPTURED_LOSTS = (
    "LOSTS:90E5B1CC2DB8:00000033,00000083,000000D4,00000124,000001C7,00000218,00000269:"
    "243F4593B8E7658FE6038C272AA9174C99146E9FD59E35C893BB5CFA5D3C0DB8"
    "7606926157DCC6D94D22DBEE00752A5FE26E91FCCA90101816BF599CE8403F44"
)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(CAPTURED_LOSTS.encode("ascii"), (ADMIN_IP, OTA_PORT))
print(f"Replayed captured valid LOSTS to {ADMIN_IP}:{OTA_PORT}")
print("Observe whether requested CHUNKs are rebroadcast. This is a known limitation if replay causes redundant traffic.")
