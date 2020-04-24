Adafruit-PiOLED-Gui-Driver
==========

Simple GUI for Adafruit PiOled screen working with i2c (https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi) and only three buttons (up, down, select) wired between 3 GPIOs on your Pi and the ground. The gpio number can be modified at the instanciation of selector_screen_btn. 

## Requirement 

```
sudo apt-get install python3-pip
sudo pip3  install RPi.GPIO
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install Pillow
```

Enable i2c
```
sudo raspi-config
```

For pillow, a fresh rpi installation will need a few libraries:
```
sudo apt-get install libopenjp2-7-dev
sudo apt-get install libtiff5-dev
```



Usage 
-----

``` 
from selector_screen_btn import Selector_screen_btn

#Creation of Screen Button Selector Object, using GPIO 20, 8 and 7 (select_btn, down_btn, up_btn)
screen_btn = Selector_screen_btn(20, 8, 7)    

``` 

Look at example.py for full example of the library
