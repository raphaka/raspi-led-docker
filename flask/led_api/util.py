import json
import sys
import os
import logging
import threading

log = logging.getLogger(__name__)

def read_json(input):
    try:
        with open(input, 'r') as infile:
                return json.loads(infile.read())
    except:
        print('ERROR: Could not load config file')
        sys.exit()

def write_json(outpath, data):
    try:
        with open(outpath, 'w') as outfile:
            json.dump(data, outfile)
        return 0
    except:
        log.error('Could not write config file')
        sys.exit()

def write_config():
    config_path = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
    return(write_json(config_path,Glob.config))

def hex_2_rgb(str_colorhex): #throws ValueError
        r=int(str_colorhex[0:2],16)
        g=int(str_colorhex[2:4],16)
        b=int(str_colorhex[4:6],16)
        return r,g,b

class Glob(object):
        config = {}
        thread_stop = True # Set to False when Thread is started. Thread checks regularly if set to True (and stop)
        current_thread = threading.Thread() #There's at max 1 thread started at each time
