from colr import Colr as C

from neopixel import *

from light_pattern import LightPattern

BLANK = (0, 0, 0)

class NeoPixelEngine(object):
    def __init__(self,
                 length: int,
                 strip: Adafruit_NeoPixel,
                 pattern: LightPattern,
                 debug: bool = False):

        self.length = length
        self.strip = strip
        self.pattern = pattern
        self.debug = debug
        self.pattern.populate_lights(self.length)

    def print_to_console(self, lights: dict) -> None:
        display = C().rgb(*BLANK, '')
        for i in range(self.length):
            if i in lights:
                rgb = lights[i]
                display += C().rgb(*rgb, '0')
            else:
                display += ' '
        print(display)

    def send_to_neopixel(self, lights: dict) -> None:
        for i in range(self.length):
            if i in lights:
                self.strip.setPixelColor(i, lights[i])

    def start(self) -> None:
        while True:
            lights = self.pattern.show()
            if self.debug:
                self.print_to_console(lights)
            else:
                self.send_to_neopixel(lights)
            self.pattern.refresh()
