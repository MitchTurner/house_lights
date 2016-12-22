# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time, timeit
import numpy as np
import lights_util as lu

from neopixel import *

# LED strip configuration:
LED_COUNT	  = 434	  # Number of LED pixels.
LED_PIN		= 18	  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA		= 5	   # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0
#LED_STRIP	  = ws.SK6812_STRIP_RGBW	
LED_STRIP	  = ws.SK6812W_STRIP


# Define functions which animate LEDs in various ways.
def twinkle(strip, spacing, min_period, max_period, fps=24):
	lights = range(0,strip.numPixels(),spacing)
	N = len(lights)
	dt = strip.numPixels()*32.0/ws.ws2811_t_freq_get(strip._leds)
	print(dt)
	
	omegas = np.random.uniform(2*np.pi/max_period, 2*np.pi/min_period, N)
	phis = np.pi*np.random.rand(N)
#	phis = np.arange(N)%2 * np.pi/2
	
	t=0

	tic = timeit.default_timer() 
	while lu.checkSwitch():
		values = np.clip(2*np.sin(omegas*t-phis)-1,0,1)**4
		whites = 100*values
		reds = 0*values
		greens = 0*values
		blues = 0*values
		t+=dt
	
		for i in range(N):
#			print(lights[i])
#			print(values[i])
			strip.setPixelColor(lights[i], Color(np.int(reds[i]),np.int(greens[i]),np.int(blues[i]),np.int(whites[i])))
		strip.show()
		time.sleep(max(0,1./fps-(timeit.default_timer()-tic)))
		tic = timeit.default_timer()

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	lu.makeSwitch()
	twinkle(strip, 2, 3, 6)  
	lu.blackOut(strip)	
