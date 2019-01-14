from random import randrange
from math import floor
from time import sleep

from engine import LightPattern, NeoPixelEngine


class RandColorBoundingLights(LightPattern):
    DIRECTIONS = [-1, 1]

    def __init__(self,
                 density: float,
                 speed: float,
                 colors: [(int, int, int)]) -> None:

        self.density = density
        self.speed = speed  # pixels a second
        self.colors = colors
        self.count = 0
        self.length = 0
        self.lights = None

    # Helper Functions
    @staticmethod
    def _random_from_list(items: [any]) -> any:
        count = len(items)
        return items[randrange(count)]

    # Abstract method implementation
    def show(self) -> dict:
        show_lights = {}
        for i in self.lights:
            show_lights[i] = self.lights[i][0]
        return show_lights

    def populate_lights(self, length: int) -> None:
        print('populating lights!')
        self.length = length
        this_count = floor(length * self.density)
        self.count = this_count
        lights = {}
        while this_count > 0:
            index = randrange(length)
            if index not in lights:
                color = self._random_from_list(self.colors)
                direction = self._random_from_list(self.DIRECTIONS)
                lights[index] = (color, direction)
                this_count -= 1
        self.lights = lights

    def refresh(self) -> None:
        old_lights = self.lights.copy()
        new_lights = {}
        for index in old_lights:
            direction = self.lights[index][1]
            new_index = index + direction
            if (new_index in self.lights) or (new_index in new_lights) or (new_index < 0) or (
                    new_index > self.length - 1):
                new_color = self._random_from_list(self.colors)
                new_direction = -direction
                self.lights[index] = (new_color, new_direction)
            else:
                new_lights[new_index] = self.lights[index]
                self.lights.pop(index)
        self.lights.update(new_lights)
        sleep(1 / self.speed)


if __name__ == '__main__':
    # GREEN = (0, 255, 0)
    # RED = (255, 0, 0)
    # YELLOW = (255, 255, 0)
    # WHITE = (255, 255, 255)
    FIRE_BOUNDS = (200, 255, 0, 255, 0, 1)
    ICY_BOUNDS = (0, 255, 0, 255, 250, 255)

    def random_color(rlower: int = 0, rupper: int = 255,
                     glower: int = 0, gupper: int = 255,
                     blower: int = 0, bupper: int = 255):
        return (randrange(rlower, rupper), randrange(glower, gupper), randrange(blower, bupper))


    color_count = 20
    bounds = FIRE_BOUNDS

    COLORS = []
    for _ in range(color_count):
        COLORS.append(random_color(*bounds))

    # LED strip configuration:
    LED_COUNT = 434  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5  # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0
    # LED_STRIP	  = ws.SK6812_STRIP_RGBW
    LED_STRIP = ws.WS2812_STRIP

    length = LED_COUNT
    density = .4
    speed = 50
    strip = Nostrip = Adafruit_NeoPixel(LED_COUNT,
                                        LED_PIN,
                                        LED_FREQ_HZ,
                                        LED_DMA,
                                        LED_INVERT,
                                        LED_BRIGHTNESS,
                                        LED_CHANNEL,
                                        LED_STRIP)

    my_pattern = RandColorBoundingLights(density, speed, COLORS)
    my_engine = NeoPixelEngine(length, strip, my_pattern, True)
    my_engine.start()
