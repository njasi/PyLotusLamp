import asyncio
import colorsys

from Controller import Controller


def time_to_rainbow_color(ms: int) -> str:
    """
    An example color state function

    just returns the hex value, later versions will have a
    choice between or maybe required to return byte array
    """
    hue = (ms % 5) / 5
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return f"{r:02x}{g:02x}{b:02x}"


async def main():
    test = Controller("UUID or Mac address")

    await test.connect()
    await test.turn_on()
    await test.set_brightness(100)

    test.apply_state_function(time_to_rainbow_color)

    # TODO make setting the function start the animation
    #       perhaps a .animate func idk

    while True:
        await test.update()
        await asyncio.sleep(0.03)


if __name__ == "__main__":
    asyncio.run(main())
