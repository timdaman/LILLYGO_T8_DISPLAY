'''
This was tested with
    CircuitPython 6.3.0
    LILYGO TTGO T8 ESP32-S2 w/Display v1.1
'''

import board
from adafruit_st7789 import ST7789
from digitalio import DigitalInOut, Direction
import displayio
import busio

class EZst7789():
    '''
    Wrapper for st7789 TFT display driver to make it easier to use on LILYGO T8 Display boards
    http://www.lilygo.cn/prod_view.aspx?TypeId=50033&Id=1321&FId=t3:50033:3

    Example usage, paints the screen green and blinks it
        from EZst7789 import EZst7789
        import displayio
        import time

        ez = EZst7789()
        ez.backlight.value = True # Turn on display backlight
        splash = displayio.Group(max_size=10)
        ez.display.show(splash)

        color_bitmap = displayio.Bitmap(ez.display.width, ez.display.height, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00 # Bright green

        bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(bg_sprite)

        backlight = ez.backlight
        while True:
            time.sleep(1)
            ez.backlight.value = False
            time.sleep(1)
            ez.backlight.value = True
    '''
    display = None
    backlight = None

    def __init__(self,
                 pin_backlight=board.LCD_BCKL,
                 clock=board.LCD_CLK,
                 mosi=board.LCD_MOSI,
                 chipselect=board.LCD_CS,
                 data_control=board.LCD_D_C,
                 reset=board.LCD_RST,
                 height=135,
                 width=240,
                 spi_baudrate=40000000
                 ):
        self._pin_backlight=pin_backlight
        self._clock=clock
        self._mosi=mosi
        self._chipselect=chipselect
        self._data_control=data_control
        self._reset=reset
        self._spi_baudrate=spi_baudrate
        self.width=width
        self.height=height
        displayio.release_displays()
        self.init_display()

    def init_display(self):
        self.backlight = DigitalInOut(self._pin_backlight)
        self.backlight.direction = Direction.OUTPUT
        self.backlight.value = False

        spi = busio.SPI(self._clock, MOSI=self._mosi)
        while not spi.try_lock():
            pass

        spi.configure(baudrate=self._spi_baudrate)
        spi.unlock()

        display_bus = displayio.FourWire(spi, command=self._data_control, chip_select=self._chipselect, reset=self._reset)
        self.display = ST7789(display_bus, rotation=90, width=self.width, height=self.height, rowstart=40, colstart=53)

        self.backlight.value = True


__author__ = "Tim Laurence"
__license__ = "GPL"
__version__ = "1.0"

