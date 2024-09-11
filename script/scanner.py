import asyncio
from bleak import BleakScanner, AdvertisementData


def rssi_to_word(rssi):
    if rssi >= -50:
        return "Excellent"
    elif rssi >= -60:
        return "Good"
    elif rssi >= -70:
        return "Fair"
    elif rssi >= -80:
        return "Poor"
    else:
        return "Very Poor"


async def pretty_discover():
    """
    Pretty print the results of BleakScanner.discover for the user

    EX:
    
    [0] DEVICE-NAME
        MAC ADDR:       mac address / uuid
        SIGNAL:         Fair (-61dBm)
        MANUFACTURER:   {...}
    """
    devices = await BleakScanner.discover(return_adv=True)

    lines = []
    for i, key in enumerate(devices):
        device, ad = devices[key]
        name = "No Name" if device.name is None else device.name.strip()

        line = (
            f"[{i}] {name}"
            f"\n\tMAC ADDR:\t{device.address}"
            f"\n\tSIGNAL:\t\t{rssi_to_word(ad.rssi)} ({ad.rssi}dBm)"
            f"\n\tMANUFACTURER:\t{ad.manufacturer_data}"
        )
        lines.append(line)

    return "\n".join(lines)


async def run():
    res = await pretty_discover()
    print(res)


if __name__ == "__main__":
    asyncio.run(run())
