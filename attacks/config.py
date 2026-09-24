# Lab configuration for your own OTA test network.
ADMIN_IP = "192.168.0.94"      # from captured HEADER admin_ip field
BROADCAST_IP = "192.168.0.255" # adjust if your /24 differs
OTA_PORT = 3333                 # TODO: replace with the real UDP OTA/LOSTS port from Wireshark
SOCKET_TIMEOUT = 2.0
