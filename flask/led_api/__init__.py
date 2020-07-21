import logging
import os
from sys import exit
from shutil import copyfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from led_api.util import Glob,read_json
from led_api.pin_controller import start_pigpio

#start flask app
app = Flask(__name__)

#handle config files, logging and pins
api_dir = os.path.dirname(os.path.realpath(__file__))
new_config_file = False
app.config.from_pyfile(api_dir + '/flask_config.cfg')
Glob.config = read_json(api_dir + '/config.json')
logging.basicConfig(filename=Glob.config['log_file'],level=Glob.config['log_level'],
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
start_pigpio()

#initialize DB and views of flask app
db = SQLAlchemy(app)
ma = Marshmallow(app)   #Wrapper to make SQLalchemy objects JSON Serializable
from led_api.views import colors,effects,setpins,settings
db.create_all()
