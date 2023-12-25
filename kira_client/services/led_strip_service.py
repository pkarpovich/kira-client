from enum import Enum


class Colors(Enum):
    Blue = (0, 0, 255)
    Green = (0, 255, 0)
    Orange = (255, 128, 0)
    Pink = (255, 51, 153)
    Purple = (128, 0, 128)
    Red = (255, 0, 0)
    White = (255, 255, 255)
    Yellow = (255, 255, 51)
    Navy = (0, 0, 128)
    SkyBlue = (135, 206, 235)
    Lime = (0, 255, 0)
    Olive = (128, 128, 0)
    Gold = (255, 215, 0)
    Coral = (255, 127, 80)
    Lavender = (230, 230, 250)
    Fuchsia = (255, 0, 255)
    Sienna = (160, 82, 45)
    Silver = (192, 192, 192)
    Off = (0, 0, 0)


class LedStripService:
    strip = None

    def __init__(self, enabled: bool, num_leds: int = 12, led_pin: int = 5):
        if not enabled:
            return

        from apa102_pi.driver.apa102 import APA102
        from gpiozero import LED

        self.strip = APA102(num_led=num_leds, global_brightness=1)
        self.power_led = LED(led_pin)
        self.num_leds = num_leds

        self.power_led.on()

    def light_up(self, color: Colors = Colors.Red):
        if not self.strip:
            return

        for i in range(self.num_leds):
            self.strip.set_pixel(i, color.value[0], color.value[1], color.value[2])

        self.strip.show()

    def clear(self):
        if not self.strip:
            return

        self.strip.clear_strip()

    def __del__(self):
        if not self.strip:
            return

        self.clear()
        self.strip.cleanup()
        self.power_led.off()
