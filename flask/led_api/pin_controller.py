import logging
import socket
import pigpio
import time
from datetime import datetime

from led_api.util import hex_2_rgb, Glob
log = logging.getLogger(__name__)

global pi

def start_pigpio():
    global pi
    if Glob.config['pins_enabled']:
        pi=pigpio.pi()

#set gpio values according to rgb-color-hex
def set_color_by_hex(colorhex):
    try:
        r,g,b = hex_2_rgb(colorhex)
    except ValueError:
        return "failed: no valid hexadecimal color value"
    return set_color(r,g,b)

#set gpio values according to rgb-color
#output value is calculated using a power function and the contrast_adjustment value in the config
#the power function always cuts 1:1 and the pitch increases as the input value gets higher
#the coordinate 1:1 is set to the brightness_maximum by multiplication
def set_color(red,green,blue):
    global pi
    c = Glob.config['contrast_adjustment']
    m = Glob.config['brightness_maximum']
    red = ((red/255) ** c)*m
    if red > 255:
        red = 255
    if red < 0:
        red = 0
    blue = ((blue/255) ** c)*m
    if blue > 255:
        blue = 255
    if blue < 0:
        blue = 0
    green = ((green/255) ** c)*m
    if green > 255:
        green = 255
    if green < 0:
        green = 0
    msg= 'setting output to:   r={0}, g={1}, b={2}'.format(red,green,blue)
    log.debug(msg)
    if Glob.config['pins_enabled']:
        pi.set_PWM_dutycycle(Glob.config['pin_red'],red)
        pi.set_PWM_dutycycle(Glob.config['pin_green'],green)
        pi.set_PWM_dutycycle(Glob.config['pin_blue'],blue)
    else:
        print(msg)
    return msg

#fades to color
def fade_to_color(start_color, target_color, duration): #duration in ms
    log.debug("fading from " + start_color + " to " + target_color + " in " + str(duration))
    fade_start = datetime.now()
    period = 1000/Glob.config['fade_frequency']
    r,g,b = hex_2_rgb(start_color)
    end_r,end_g,end_b = hex_2_rgb(target_color)
    duration = duration / Glob.config["effect_speed"]
    num_steps = int(duration / period)
    if num_steps > 0:  #only execute if theres at least one step in fade progress
        step_r = (end_r-r)/num_steps
        step_g = (end_g-g)/num_steps
        step_b = (end_b-b)/num_steps
        periodseconds = period/1000 #saved to value, so this division is not performed every loop
        for x in range(0, num_steps):
            time_start = datetime.now()
            if (Glob.thread_stop == True):
                logging.info('fade: Terminating - Stop flag has been set')
                return 1
            r = r + step_r
            if r > 255:
                r = 255
            if r < 0:
                r = 0
            g = g + step_g
            if g > 255:
                g = 255
            if g < 0:
                g = 0
            b = b + step_b
            if b > 255:
                b = 255
            if b < 0:
                b = 0
            set_color(r,g,b)
            exec_time = datetime.now() - time_start
            if (periodseconds > exec_time.total_seconds()):
                time.sleep(periodseconds - exec_time.total_seconds())
    time.sleep((duration % period)/1000) #correction if period is not a whole multiple of duration
    set_color_by_hex(target_color)
    actual_duration = datetime.now() - fade_start
    return 0
