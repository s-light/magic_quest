# SPDX-FileCopyrightText: 2024 Ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of sending and recieving data with the RFM9x or RFM69 radios.
# Author: Jerry Needell

import board
import busio
import digitalio

# Define radio parameters.
RADIO_FREQ_MHZ = 433.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

print("rfm69 init")
CS = digitalio.DigitalInOut(board.D10)
RESET = digitalio.DigitalInOut(board.D9)

# Initialze RFM radio
# Use rfm69 for two RFM69 radios using FSK

from adafruit_rfm import rfm69

# rfm = rfm69.RFM69(spi=board.SPI(), CS, RESET, RADIO_FREQ_MHZ)
rfm = rfm69.RFM69(
    spi=board.SPI(),
    cs=CS,
    rst=RESET,
    frequency=433.0,
)

# For RFM69 only: Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
# rfm.encryption_key = None
# rfm.encryption_key = (
#    b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
# )

# for OOK on RFM69 or RFM9xFSK
# rfm.modulation_type = 1

# Send a packet.  Note you can only send a packet containing up to 60 bytes for an RFM69
# and 252 bytes forn  an RFM9x.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm.send(bytes("Hello world!\r\n", "utf-8"))
print("Sent Hello World message!")

# Wait to receive packets.
print("Waiting for packets...")

while True:
    packet = rfm.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    # packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been received
        print("Received nothing! Listening again...")
    else:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print(f"Received (raw bytes): {packet}")
        # And decode to ASCII text and print it too.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        try:
            packet_text = str(packet, "ascii")
            print(f"Received (ASCII): {packet_text}")
        except UnicodeError:
            print("Hex data: ", [hex(x) for x in packet])
        # Also read the RSSI (signal strength) of the last received message and
        # print it.
        rssi = rfm.last_rssi
        print(f"Received signal strength: {rssi} dB")

    if int(time.monotonic() * 10) % 10 == 0:
        rfm.send(bytes("Hello world!\r\n", "utf-8"))
        print("Sent Hello World message!")
