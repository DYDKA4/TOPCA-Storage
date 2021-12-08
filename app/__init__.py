from flask import Flask
import logging
import datetime


app = Flask(__name__)
now = datetime.datetime.now()
logging.basicConfig(filename=f'logs/record_{now.strftime("%d-%m-%Y_%H:%M")}.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from app import views
