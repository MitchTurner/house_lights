from neopixel import *
import math
import time
import numpy as np

LED_COUNT	  = 434	  # Number of LED pixels.
LED_PIN		= 18	  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA		= 5	   # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0
LED_STRIP	  = ws.SK6812_STRIP_RGBW

SPACE_PERIOD = 10.0
TIME_PERIOD = 4.0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

dt = 1/24.0
G = 200
braneSpacing = 20
boundary = LED_COUNT/2.0

m = [1.0,1.0,1.0,1.0]
x = np.random.rand(1,4) * 2.0* boundary - boundary
v = [0.0, 0.0, 0.0,0.0];

if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()

    while True:
        t = time.time()

	for massCounter in xrange(4):
		#flush
		accelerations = [0.0, 0.0, 0.0, 0.0]
		
		#Calculation accelerations
		for notIndex in xrange(4):
			if notIndex != massCounter :
				accelerations[massCounter] = ( 
					np.sign( x[0][notIndex] - x[0][massCounter] ) * 
					G * m[notIndex]
#Comment the next two lines and reduce G, perhaps to 10 (from 300) for 1-D gravity 
					/
					( (x[0][notIndex] - x[0][massCounter])**2 + braneSpacing**2) 
					)

		#At the edge? bounce
		if abs( x[0][massCounter] ) > boundary :
			v[massCounter] = v[massCounter] * -1;

		#Aggregate accelerations, Euler round one.
		v[massCounter] = v[massCounter] + np.sum(accelerations) * dt
	
	#Step Forward with Euler round two
	x = np.add( x , np.multiply(v, dt))

	#Display begins
        for i in xrange(strip.numPixels()):
	    pixel  = [0, 0, 0, 0];
	    if abs( i - ( x[0][0] + boundary ) ) < 3 :
		pixel[0] += 255;
	    if abs( i - (x[0][1] + boundary) ) < 3 :
		pixel[1] += 255;
	    if abs( i - (x[0][2] + boundary) ) < 3 :
		pixel[2] += 255;
	    if abs( i - (x[0][3] + boundary) ) < 3 :
		pixel[3] += 255;
            strip.setPixelColorRGB(i, pixel[0], pixel[1], pixel[2], pixel[3] )
        strip.show()
        time.sleep(dt)
