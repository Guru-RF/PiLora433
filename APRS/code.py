import time
from datetime import datetime
import board
import busio
from digitalio import DigitalInOut, Direction
import asyncio
import random
import config

import sys
sys.path.append('./lib')
import adafruit_rfm9x
from APRS import APRS

# our version
VERSION = "RF.Guru_APRSGateway4PI 0.1" 

print(f"{config.call} -=- {VERSION}\n")

async def loraRunner(loop):
    # LoRa APRS frequency
    RADIO_FREQ_MHZ = 433.775
    CS = DigitalInOut(board.D7)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000, agc=False,crc=True)

    while True:
        await asyncio.sleep(0)
        stamp = datetime.now()
        print(f"{stamp}: [{config.call}] loraRunner: Waiting for lora APRS packet ...\r", end="")
        timeout = int(config.timeout) + random.randint(1, 9)
        packet = rfm9x.receive(with_header=True,timeout=timeout)
        if packet is not None:
            if packet[:3] == (b'<\xff\x01'):
                try:
                    rawdata = bytes(packet[3:]).decode('utf-8')
                    stamp = datetime.now()
                    print(f"\r{stamp}: [{config.call}] loraRunner: RSSI:{rfm9x.last_rssi} SNR:{rfm9x.last_snr} Data:{rawdata}")
                    wifi.pixel_status((100,100,0))
                    loop.create_task(tcpPost(rawdata))
                    if config.enable is True:
                        loop.create_task(httpPost(rawdata,rfm9x.last_rssi,rfm9x.last_snr))
                    wifi.pixel_status((0,100,0))
                except:
                    print(f"{stamp}: [{config.call}] loraRunner: Lost Packet, unable to decode, skipping")
                    continue


async def main():
   loop = asyncio.get_event_loop()
   loraR = asyncio.create_task(loraRunner(loop))
   #loraA = asyncio.create_task(iGateAnnounce())
   #await asyncio.gather(loraR, loraA)
   await asyncio.gather(loraR)


asyncio.run(main())