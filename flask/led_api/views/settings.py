import logging
from flask import request, jsonify

from led_api.util import Glob, write_config
from led_api import app

log = logging.getLogger(__name__)

#retrieve new config
#or update the sent values on server side
@app.route('/settings', methods = ['GET', 'PUT'])
def res_settings():
    if request.method == 'PUT':
        if not request.content_type == 'application/json':
            return ('failed: Content type must be application/json', 401)
        data = request.get_json()
        invalid_keys = []
        for k in data:
            # check data type and insert in settings if correct
            if (k in ["brightness_maximum","pin_blue","pin_green","pin_red","udp_port"]):
                if (isinstance(data[k], int) and data[k] > 0):
                    Glob.config[k] = data[k]
                else:
                    invalid_keys.append(k)
            elif (k in ["contrast_adjustment","effect_speed","fade_frequency","socket_timeout"]):
                if (isinstance(data[k], float) or isinstance(data[k], int)):
                    Glob.config[k] = data[k]
                else:
                    invalid_keys.append(k)
            elif (k in ["log_file"]):
                if (isinstance(data[k], str)):
                    Glob.config[k] = data[k]
                else:
                    invalid_keys.append(k)
            elif (k in ["log_level"]):
                if (data[k] in ["NOTSET","DEBUG","INFO","WARNING","ERROR","CRITICAL"]):
                    Glob.config[k] = data[k]
                else:
                    invalid_keys.append(k)
            elif (k in ["pins_enabled"]):
                if (isinstance(data[k], bool)):
                    Glob.config[k] = data[k]
                else:
                    invalid_keys.append(k)
            else:
                invalid_keys.append(k)
        if (write_config() == 0):
            log.info('updated config file')
        else:
            return('failed: Could not write settings to output file', 500)
        if (not invalid_keys):
            return 'success'
        else:
            return (jsonify(invalid_keys),400)
    else:
        return jsonify(Glob.config)
