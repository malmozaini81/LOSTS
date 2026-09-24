# Secure Stateless UDP Broadcast Protocol for ESP32-S3 OTA

This repository contains the implementation, formal verification model,
experimental tools, and supporting evidence for a secure UDP broadcast
over-the-air (OTA) firmware update protocol for ESP32-S3 devices.

The protocol is designed for one-to-many firmware distribution over a local
Wi-Fi network. The administrator broadcasts a firmware image once to all
participating devices rather than maintaining a separate OTA session for each
device. Devices independently detect missing chunks and request selective
recovery when required.

## Protocol Overview

The OTA process consists of the following main operations:

1. The administrator signs and broadcasts a firmware HEADER containing the
   firmware version, image size, chunk configuration, and SHA-256 digest.

2. Each ESP32-S3 verifies the administrator's ECDSA signature and checks the
   firmware version before accepting the update.

3. The firmware is divided into chunks of up to 1400 bytes and distributed
   using UDP broadcast.

4. Each CHUNK contains an index and CRC32 value. Devices independently verify
   received chunks and track missing chunks.

5. If chunks remain missing after the configured inactivity period, the device
   sends an ECDSA-signed recovery request directly to the administrator.

6. After authenticating the device request, the administrator rebroadcasts
   the requested chunks.

7. When all chunks have been received, the ESP32-S3 verifies the reconstructed
   firmware using SHA-256 before writing it to the inactive OTA partition.

The administrator does not maintain per-device firmware reception state or
per-device OTA sessions.

## Security Mechanisms

The implementation uses:

- ECDSA authentication of firmware metadata
- ECDSA authentication of recovery requests
- SHA-256 verification of the reconstructed firmware image
- CRC32 verification of individual firmware chunks
- Firmware version checking for downgrade protection
- ESP-IDF OTA partition and rollback mechanisms

## Formal Verification

The repository includes the ProVerif 2.05 model used to formally analyze the
protocol under the Dolev–Yao adversary model.

The formal analysis evaluates:

- Firmware injection through firmware-authenticity verification
- Forged recovery requests through recovery-request authentication
- Request flooding at the authentication level using replicated request handling
- Firmware tampering through firmware-integrity verification
- Downgrade attacks through firmware-freshness verification
- Recovery-request replay through injective recovery authentication

ProVerif verified firmware authenticity, recovery-request authentication,
firmware integrity, and firmware freshness. Under replicated recovery-request
handling, forged requests could not reach authenticated recovery processing.

The injective recovery-authentication query identified a replay limitation:
a previously valid signed recovery request can be processed more than once,
potentially causing redundant chunk rebroadcast.

The ProVerif model and corresponding verification results are included with
the project files.

## Practical Security Evaluation

The implemented system was also evaluated using practical attack experiments.

Six attack scenarios were tested:

- Forged recovery request
- Request flooding
- Firmware injection
- Downgrade attack
- Replay attack
- Chunk tampering

The practical evaluation showed that forged recovery requests, unauthorized
firmware injection, downgrade attempts, and corrupted chunks were rejected by
the implemented security mechanisms. Under the evaluated flooding condition,
forged requests were continuously rejected without triggering unauthorized
recovery and without a substantial observed system-level CPU load.

The replay experiment reproduced the limitation identified by the formal
analysis: a previously captured valid recovery request can be accepted and can
trigger redundant chunk rebroadcast. This does not bypass firmware
authentication or cause unauthorized firmware installation.

## Experimental Evidence

Supporting material for the practical security experiments is provided in this
repository, including:

- Attack scripts
- Wireshark packet captures (`.pcapng`)
- Administrator console logs
- ESP32-S3 serial logs
- Supporting screenshots

These artifacts provide the network-level and endpoint-level evidence used in
the practical security evaluation.

## Experimental Platform

The implementation and evaluation use:

- ESP32-S3 devices
- ESP-IDF v6.0.1
- Python-based OTA administrator
- Wi-Fi UDP broadcast for firmware distribution
- UDP unicast for authenticated recovery requests
- Wireshark for packet capture
- ProVerif 2.05 for formal verification

The practical security experiments use a Microsoft Surface Pro 7 as the
attacker machine. Network traffic is independently captured using Wireshark
running on a Linux Mint 22.3 virtual machine equipped with an Alfa AWUS036ACH
wireless adapter.

## Repository Structure

The repository contains the protocol implementation and supporting research
artifacts. Practical security evidence is organized by attack scenario so that
the attack scripts, packet captures, and corresponding endpoint logs can be
examined together.

## Research Use

This repository accompanies the research work:

**Secure Stateless UDP Broadcast Protocol for ESP32-S3 OTA**

The repository is intended to support reproducibility and provide access to
the implementation, formal verification model, and experimental evidence
reported in the associated research paper.
