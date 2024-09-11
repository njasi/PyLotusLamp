import asyncio
import logging
import time
from bleak import BleakClient
from CommandUtils import CommandUtils


logging.basicConfig(
    level=logging.INFO, format=f"%(asctime)s - %(name)s %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
# set the logging level to DEBUG to see all responses
logger.setLevel(logging.INFO)


class Controller:
    """
    A class to control a single LED device.
    """

    def __init__(
        self,
        address,
        write_characteristic=None,
        notify_characteristic=None,
        notif_handler=None,
    ):
        """
        Create a new controller from provided address

        address: str                    mac address of the device
        write_characteristic: str       characteristic uuid to write commands to,
                                        if not supplied controler will scan for one
        notify_characteristic: str      characteristic uuid to recieve notifications on,
                                        if not supplied controler will scan for one
        notif_handler: function         handler to deal with notifications
        """
        self.device_address = address

        # characteristics to track
        self._write_uuid = write_characteristic
        self._notify_uuid = notify_characteristic

        self.notif_handler = notif_handler

        # state things I guess
        self.color = None
        self.brightness = None
        self.speed = None
        self.pattern = None
        self.power = False

        self._state_function = None
        self._task = None
        self._delta_t = 0.02

        # self._color_b_arr

    async def connect(self):
        """
        Start a connection to the client

        try to pair & search for the correct characteristics
        """
        self.client = BleakClient(self.device_address)
        await self.client.connect()
        if self.client.is_connected:
            logger.debug(f"[{self.device_address}] Connected")
        else:
            logger.error(f"[{self.device_address}] Connection Failed")

        try:
            paired = await self.client.pair()
            if paired:
                logger.debug(f"[{self.device_address}] Device paired successfully")
            else:
                logger.error(f"[{self.device_address}] Failed to pair with device")

        except NotImplementedError as e:
            logger.error("Mac device, cannot initiate pairing.")
            pass
            # raise e

        await self._scan_services_characteristics()

        if self._notify_uuid is not None:
            await self.client.start_notify(
                self._notify_uuid, self._handle_notifications()
            )

    def _handle_notifications(self):
        """
        generate a function to handle the notifs
        """

        def generated(sender, data):
            logger.debug(
                f"[{self.device_address}] Notification from {sender}: {data.hex()}"
            )
            if self.notif_handler is not None:
                self.notif_handler(sender, data)

        return generated

    async def _scan_services_characteristics(self):
        """
        Scan the device for it's characteristics & services.

        for now assume whichever one allows writing is the correct one lol
        """
        for service in self.client.services:
            logger.debug(f"[{self.device_address}] Service: {service.uuid}")
            for characteristic in service.characteristics:
                logger.debug(
                    f"[{self.device_address}] Characteristic: {characteristic.uuid}\n\tProperties:{characteristic.properties}\n"
                )
                for prop in characteristic.properties:
                    if self._write_uuid is None and "write" in prop:
                        self._write_uuid = characteristic.uuid
                    if self._notify_uuid is None and "notify" in prop:
                        self._notify_uuid = characteristic.uuid

    async def send_bytes(self, cmd_bytes):
        """
        TODO account for devices which actually write back
        """
        return await self.client.write_gatt_char(
            self._write_uuid, cmd_bytes, response=False
        )

    async def ping(self, cmd_bytes=bytes([0x00])):
        """
        Send a command to keep the connection going

        bytes: Buffer   this should be nonesense (or if your device actually had a ping protocol use that lol)
        """
        await self.send_bytes(cmd_bytes)

    async def set_color(self, r, g, b):
        """
        Send the color & update self state
        """
        self.color = (r, g, b)
        cmd_bytes = CommandUtils.create_color_command(r, g, b)
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set color to R: {r}, G: {g}, B: {b}")

    async def set_color_hex(self, hex):
        """
        Send the color & update self state but with hex code
        """
        self.color = hex
        cmd_bytes = CommandUtils.create_color_command_bytes(bytearray.fromhex(hex))
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set color to {hex}")

    async def set_brightness(self, value):
        """
        Send the brightness & update self state
        """
        self.brightness = value
        cmd_bytes = CommandUtils.create_brightness_command(value)
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set brightness to: {value}")

    async def set_speed(self, value):
        """
        Send new speed & update self state
        """
        self.speed = value
        cmd_bytes = CommandUtils.create_speed_command(value)
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set speed to: {value}")

    async def set_pattern(self, value):
        """
        Send new pattern & update self state
        """
        self.pattern = value
        cmd_bytes = CommandUtils.create_pattern_command(value)
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set pattern to: {value}")

    async def set_power(self, power):
        """
        Send the power on/off command to device
        """
        self.power = power
        cmd_bytes = CommandUtils.create_on_off_command(power)
        await self.send_bytes(cmd_bytes)
        logger.debug(f"[{self.device_address}] Set power to: {power}")

    async def turn_on(self):
        """
        Turn the device power off
        """
        await self.set_power(True)

    async def turn_off(self):
        """
        Turn the device power on
        """
        await self.set_power(False)

    async def toggle_power(self):
        """
        Toggle the power state on/off
        """
        await self.set_power(not self.power)

    def set_state_function(self, cb):
        """
        Set the state function; a function which returns a color given the time

        # TODO add brightness and other state control as well
        """
        self._state_function = cb

    async def _state_loop(self):
        """
        State loop wrapper
        """
        while True:
            await asyncio.sleep(self._delta_t)
            color = self._state_function(time.time())
            await self.set_color_hex(color)

    def start_state_loop(self, delta_t=0.02):
        """
        Start the state loop

        delta_t, float  the time between update steps
        """
        self._delta_t = delta_t

        if self._state_function is None:
            # TODO raise error instead
            return

        self._task = asyncio.create_task(self._state_loop())

    def stop_state_loop(self):
        """
        Stop the state loop
        """

        if self._task is None:
            # TODO raise error instead
            return

        self._task.cancel()
        self._task = None
