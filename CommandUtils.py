class CommandUtils:
    """
    Basic command generation
    """

    @staticmethod
    def create_on_off_command(is_on: bool) -> bytes:
        return bytes(
            [
                0x7E,
                0x04,
                0x04,
                0x01 if is_on else 0x00,
                0x00,
                0x01 if is_on else 0x00,
                0xFF,
                0x00,
                0xEF,
            ]
        )

    @staticmethod
    def create_color_command(
        red_value: int, green_value: int, blue_value: int
    ) -> bytes:
        return bytes(
            [0x7E, 0x07, 0x05, 0x03, red_value, green_value, blue_value, 0x10, 0xEF]
        )

    def create_color_command_bytes(hex: bytes):
        return bytes([0x7E, 0x07, 0x05, 0x03, *hex, 0x10, 0xEF])

    @staticmethod
    def create_pattern_command(pattern: int) -> bytes:
        pattern = max(0, min(28, pattern))  # Ensure pattern is between 0 and 28
        return bytes([0x7E, 0x05, 0x03, pattern + 128, 0x03, 0xFF, 0xFF, 0x00, 0xEF])

    @staticmethod
    def create_speed_command(speed: int) -> bytes:
        # TODO: this doesn't seem to work for the melk oc21 device I have
        speed = max(0, min(100, speed))  # Ensure speed is between 0 and 100
        return bytes([0x7E, 0x04, 0x02, speed, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])

    @staticmethod
    def create_brightness_command(brightness: int) -> bytes:
        brightness = max(
            0, min(100, brightness)
        )  # Ensure brightness is between 0 and 100
        return bytes([0x7E, 0x04, 0x01, brightness, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])

    # untested
    @staticmethod
    def create_mic_on_off_command(is_on: bool) -> bytes:
        return bytes(
            [0x7E, 0x04, 0x07, 0x01 if is_on else 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0xEF]
        )

    # untested
    @staticmethod
    def create_mic_eq_command(eq_mode: int) -> bytes:
        eq_mode = max(0, min(3, eq_mode))  # Ensure eq_mode is between 0 and 3
        return bytes([0x7E, 0x05, 0x03, eq_mode + 128, 0x04, 0xFF, 0xFF, 0x00, 0xEF])

    # untested
    @staticmethod
    def create_mic_sensitivity_command(sensitivity: int) -> bytes:
        sensitivity = max(
            0, min(100, sensitivity)
        )  # Ensure sensitivity is between 0 and 100
        return bytes([0x7E, 0x04, 0x06, sensitivity, 0xFF, 0xFF, 0xFF, 0x00, 0xEF])
