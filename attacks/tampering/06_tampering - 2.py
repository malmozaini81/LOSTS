"""Test: temper attack.
Expected with the current design: device will refuse the chunk.
"""
import socket
import os

OTA_PORT = 3333                 
BROADCAST_IP = "192.168.0.255"

TRIGGER_CHUNK = 550
ATTACK_CHUNK = 600

trigger_hex = f"{TRIGGER_CHUNK:08X}".encode()
attack_hex = f"{ATTACK_CHUNK:08X}".encode()

rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rx.bind(("", OTA_PORT))

tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Waiting for administrator OTA broadcast...")

while True:
    packet, addr = rx.recvfrom(65535)

    if not packet.startswith(b"CHUNK:"):
        continue

    try:
        parts = packet.split(b":", 3)
        index = int(parts[1], 16)
    except (ValueError, IndexError):
        continue

    print(f"Observed administrator CHUNK {index}")

    if index == TRIGGER_CHUNK:

        malicious_data = os.urandom(1400)

        # Deliberately incorrect CRC.
        fake_crc = b"DEADBEEF"

        malicious_packet = (
            b"CHUNK:"
            + attack_hex
            + b":"
            + fake_crc
            + b":"
            + malicious_data
        )

        tx.sendto(malicious_packet, (BROADCAST_IP, OTA_PORT))
        tx.sendto(malicious_packet, (BROADCAST_IP, OTA_PORT))

        print(f"\nATTACK: injected CHUNK {ATTACK_CHUNK}")
        print(f"Triggered after observing CHUNK {TRIGGER_CHUNK}")
        print("CRC deliberately invalid")
        print("Waiting for genuine administrator CHUNK 600...\n")

        # Continue listening instead of exiting.
        while True:
            genuine, genuine_addr = rx.recvfrom(65535)

            if genuine.startswith(b"CHUNK:" + attack_hex + b":"):
                print("Genuine administrator CHUNK 600 subsequently observed.")
                break

        break
