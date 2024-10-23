import sys
import datetime
import argparse
import asyncio
from bms import BMS
import dataclasses
import logging
import json

logger = logging.getLogger("signalk-123smartbms-usb")


@dataclasses.dataclass
class ComInstance:
    id: str
    port: str
    bms: BMS


async def monitor(config):
    instances = []
    loop = asyncio.get_running_loop()

    for device in config["devices"]:
        bms = BMS(loop, device["port"])
        await bms.connect()
        com = ComInstance(device["port"], device["id"], bms)
        instances.append(com)

    while True:
        for instance in instances:
            delta = {
                "updates": {
                    "source": {
                        "label": "123/Smart BMS",
                        "type": "USB",
                        "src": instance.port,
                    },
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "values": {
                        f"electrical.batteries.{instance.id}.voltage": str(instance.bms.pack_voltage),
                        f"electrical.batteries.{instance.id}.voltage": str(instance.bms.pack_current),
                        f"electrical.batteries.{instance.id}.stateOfCharge": str(instance.bms.soc),
                        f"electrical.batteries.{instance.id}.lowestCellVoltage": str(instance.bms.lowest_cell_voltage),
                        f"electrical.batteries.{instance.id}.highestCellVoltage": str(instance.bms.highest_cell_voltage),
                        f"electrical.batteries.{instance.id}.allowedToCharge": str(int(instance.bms.allowed_to_charge)),
                        f"electrical.batteries.{instance.id}.allowedToDischarge": str(int(instance.bms.allowed_to_discharge)),
                        f"electrical.batteries.{instance.id}.communicationError": str(
                            int(
                                instance.bms.cell_communication_error
                                or instance.bms.serial_communication_error
                            )
                        ),
                    },
                }
            }

            logger.info(delta)
            print(json.dumps(delta))
            sys.stdout.flush()

        await asyncio.sleep(3)


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--verbose", "-v", action="store_true", help="Increase the verbosity"
    )
    args = p.parse_args()

    logging.basicConfig(
        stream=sys.stderr, level=logging.DEBUG if args.verbose else logging.WARNING
    )

    logging.debug("Waiting for config...")
    config = json.loads(input())
    logging.info("Configured: %s", json.dumps(config))
    asyncio.run(monitor(config))


if __name__ == "__main__":
    main()
