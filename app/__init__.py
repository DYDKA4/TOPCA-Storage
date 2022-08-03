from flask import Flask
import logging
import datetime
import os

app = Flask(__name__)
now = datetime.datetime.now()
if not os.path.exists(f'logs/{now.strftime("%d-%m-%Y")}'):
    os.mkdir(f'logs/{now.strftime("%d-%m-%Y")}')

logging.basicConfig(filename=f'logs/{now.strftime("%d-%m-%Y")}/record_{now.strftime("%d-%m-%Y_%H%M")}.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from app import views

